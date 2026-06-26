#!/usr/bin/env python3
"""Append a resolution to the pronoun-resolver ledger (locked, atomic).

Called by Claude after it resolves an ambiguous reference, per the directive the
detect-pronouns.sh hook injects. Never store raw prompt text — only a hash.

All free-text fields are sanitized (secret/PII redaction + length caps) and the
whole read-modify-write runs under an exclusive file lock so concurrent hook
fires can't drop each other's entries.

Examples:
  log-resolution.py --ledger PATH --pronoun it --resolved-to "the auth middleware" \
      --tier green --confidence 0.92
  log-resolution.py --ledger PATH --correct-last      # mark prior entry corrected
"""
import argparse, fcntl, json, math, os, re, sys, datetime, tempfile
from contextlib import contextmanager

DEFAULT_LEDGER = os.path.join(os.path.dirname(__file__), "..", ".claude", "pronoun-ledger.json")

MAX_LEN = 120          # referents are short noun phrases; longer values are suspect
MAX_PRONOUN_LEN = 40   # the token itself ("it", "that other one") is always short

# prompt_hash must look like a hex digest (sha-256 = 64 chars); reject anything else
# so a mistaken caller can't smuggle raw prompt text through this field.
HASH_RE = re.compile(r"^[0-9a-fA-F]{32,128}$")

# Secret / PII patterns — match anywhere in the value and redact the whole value.
SECRET_PATTERNS = [
    r"sk-[A-Za-z0-9_-]{16,}",            # OpenAI-style
    r"sk_live_[A-Za-z0-9]{16,}",         # Stripe live
    r"sk_test_[A-Za-z0-9]{16,}",         # Stripe test
    r"rk_live_[A-Za-z0-9]{16,}",         # Stripe restricted
    r"whsec_[A-Za-z0-9]{16,}",           # Stripe/webhook signing secret
    r"gh[pousr]_[A-Za-z0-9]{20,}",       # GitHub tokens
    r"github_pat_[A-Za-z0-9_]{20,}",     # GitHub fine-grained PAT
    r"glpat-[A-Za-z0-9_-]{16,}",         # GitLab PAT
    r"xox[baprs]-[A-Za-z0-9-]{10,}",     # Slack bot/user tokens
    r"xox[ce]-[A-Za-z0-9-]{10,}",        # Slack browser/export tokens
    r"xapp-[A-Za-z0-9-]{10,}",           # Slack app-level token
    r"npm_[A-Za-z0-9]{20,}",             # npm automation token
    r"AKIA[0-9A-Z]{16}",                 # AWS access key id
    r"ASIA[0-9A-Z]{16}",                 # AWS temp key id
    r"AIza[0-9A-Za-z_-]{30,}",           # Google API key
    r"ya29\.[0-9A-Za-z_-]{20,}",         # Google OAuth token
    r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",  # JWT
    r"-----BEGIN[A-Z ]+PRIVATE KEY-----",                              # PEM private key
    r"[a-zA-Z][a-zA-Z0-9+.-]*://[^/\s:@]+:[^/\s:@]+@",                 # creds in a URL (postgres://u:p@)
    r"\b(?i:bearer|basic)\s+[A-Za-z0-9._=+/-]{12,}",                   # Bearer/Basic auth header
    r"(?i:api[_-]?key|secret|token|password|passwd|pwd)\s*[:=]\s*\S+",  # key=value secrets
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",             # email address
    r"\b\d{3}-\d{2}-\d{4}\b",                                          # US SSN
    r"\b(?:\+?\d[\s.-]?){10,15}\b",                                    # phone number
    r"\b(?:\d[ -]?){13,19}\b",                                         # credit-card-ish digit run
    r"\b[0-9a-fA-F]{32,}\b",                                           # long hex blob (keys/hashes)
    r"[A-Za-z0-9+/]{40,}={0,2}",                                       # long base64 blob (no trailing \b)
]
_SECRET_RE = re.compile("|".join(SECRET_PATTERNS))
_CTRL_RE = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")  # control chars except \t,\n,\r

REDACTED = "[redacted: possible secret/PII]"


def sanitize(value, max_len=MAX_LEN):
    """Redact secret/PII-looking free-text before it ever touches disk.

    Returns (clean_value, was_redacted). Conservative: any secret-pattern match
    replaces the whole field; control chars are stripped; overly long values are
    truncated (a long value is itself a red flag for a non-referent).
    """
    if not value:
        return value, False
    if _SECRET_RE.search(value):
        return REDACTED, True
    cleaned = _CTRL_RE.sub("", value)
    changed = cleaned != value
    if len(cleaned) > max_len:
        return cleaned[:max_len].rstrip() + "… [truncated]", True
    return cleaned, changed


def clean_confidence(c):
    """Clamp to [0,1]; reject nan/inf (which json would emit as invalid JSON)."""
    if c is None or not math.isfinite(c):
        return 0.5
    return max(0.0, min(1.0, c))


def clean_hash(h):
    """Keep only genuine hex digests; drop anything else (e.g. raw prompt text)."""
    return h if (h and HASH_RE.match(h)) else ""


def _empty():
    return {
        "version": 1,
        "adaptive_threshold": 0.8,
        "resolution_count": 0,
        "context_reliability": {
            "last_edited_file": 0.5, "last_tool_call": 0.5,
            "conversation_topic": 0.5, "recent_symbol": 0.5,
        },
        "resolutions": [],
    }


EMPTY = _empty()


def _backup_corrupt(path):
    """Move a non-empty, unusable ledger aside so we never silently destroy data."""
    try:
        if os.path.exists(path) and os.path.getsize(path) > 0:
            os.replace(path, path + ".corrupt")
            print(f"warning: unusable ledger backed up to {path}.corrupt", file=sys.stderr)
    except OSError:
        pass


def load(path):
    try:
        with open(path) as f:
            d = json.load(f)
    except FileNotFoundError:
        return _empty()
    except (OSError, ValueError):
        # Existing but unparseable: preserve it instead of silently overwriting,
        # so a transient parse error / manual edit doesn't destroy the ledger.
        _backup_corrupt(path)
        return _empty()
    if not isinstance(d, dict):
        # Valid JSON but wrong shape (e.g. a list) — also back up before resetting.
        _backup_corrupt(path)
        return _empty()
    d.setdefault("resolutions", [])
    d.setdefault("resolution_count", len(d["resolutions"]))
    return d


def save(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path) or ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f, indent=2, allow_nan=False)  # allow_nan=False: never write NaN/Infinity
        os.replace(tmp, path)  # atomic within the same directory
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


@contextmanager
def _lock(path):
    """Exclusive lock over the whole read-modify-write to prevent lost updates."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    lf = open(path + ".lock", "w")
    try:
        fcntl.flock(lf, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(lf, fcntl.LOCK_UN)
        lf.close()


def update_ledger(path, mutate):
    """Load -> mutate(led) -> save, all under an exclusive lock. Returns the ledger."""
    with _lock(path):
        led = load(path)
        mutate(led)
        led["resolution_count"] = len(led.get("resolutions", []))
        save(path, led)
        return led


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", default=DEFAULT_LEDGER)
    ap.add_argument("--pronoun")
    ap.add_argument("--resolved-to")
    ap.add_argument("--tier", choices=["green", "yellow", "red", "black"])
    ap.add_argument("--confidence", type=float)
    ap.add_argument("--context-signal", default="")
    ap.add_argument("--prompt-hash", default="")
    ap.add_argument("--correct-last", action="store_true",
                    help="mark the most recent resolution as was_corrected")
    args = ap.parse_args()

    if args.correct_last:
        found = {"v": False}

        def _mark(led):
            if led.get("resolutions"):
                led["resolutions"][-1]["was_corrected"] = True
                found["v"] = True

        update_ledger(args.ledger, _mark)
        print("Marked last resolution corrected." if found["v"]
              else "No resolutions to correct.",
              file=sys.stdout if found["v"] else sys.stderr)
        return

    if not (args.pronoun and args.resolved_to and args.tier):
        ap.error("--pronoun, --resolved-to, and --tier are required when logging a resolution")

    pronoun, r0 = sanitize(args.pronoun, max_len=MAX_PRONOUN_LEN)
    resolved_to, r1 = sanitize(args.resolved_to)
    context_signal, r2 = sanitize(args.context_signal)
    if r0 or r1 or r2:
        print("note: redacted possible secret/PII before logging.", file=sys.stderr)

    entry = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "pronoun": pronoun,
        "resolved_to": resolved_to,
        "tier_used": args.tier,
        "confidence": clean_confidence(args.confidence),
        "context_signal_used": context_signal,
        "was_corrected": False,
        "prompt_hash": clean_hash(args.prompt_hash),
    }
    led = update_ledger(args.ledger, lambda l: l["resolutions"].append(entry))
    print(f"Logged resolution #{led['resolution_count']}: {pronoun} -> {resolved_to} ({args.tier})")


if __name__ == "__main__":
    main()
