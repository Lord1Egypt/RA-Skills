#!/usr/bin/env python3
"""
Trace Extractor v2 — LLM-powered extraction from session traces and daily notes.

Instead of noisy regex patterns, uses the LLM to semantically extract:
  1. DECISIONS — new choices made, things decided or changed
  2. ERRORS — bugs, failures, workarounds discovered
  3. FACTS — new information learned (versions, configs, status changes)
  4. PATTERNS — recurring themes worth tracking

Output:
  - Updates memory/YYYY-MM-DD.md with extracted items
  - Appends new entities to memory/ontology/graph.jsonl
  - Flags items that should be promoted to MEMORY.md
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# Model resolution is centralised in llm_resolution.py (v4.0). The old hard-coded
# names (`deepseek-v4.1-flash:cloud` for cloud, `qwen2.5:7b` for the local
# fallback) are gone: both now come from the shared module. The local model
# survives ONLY as the last link of the shared chain, and its presence is
# validated before use (spec v4 section 6.1 — never hang on a synchronous pull).
_HERE = Path(__file__).resolve().parent
# The shared resolver lives in hybrid-search/. Look for it in every location this
# file can be deployed to (repo, installed skill, standalone skill dir) so the
# import never silently degrades to the old hard-coded fallback.
for _cand in (
    _HERE / "hybrid-search",                                  # repo layout
    _HERE,                                                      # module sits beside us
    _HERE.parent / "memory-health" / "hybrid-search",           # sibling installed skill
):
    if (_cand / "llm_resolution.py").is_file():
        sys.path.insert(0, str(_cand))
        break
try:
    from llm_resolution import (
        resolve_llm_model as _resolve_llm_model,
        fallback_model as _fallback_model,
    )
    _HAVE_LLM_RESOLUTION = True
except ImportError:  # pragma: no cover - defensive: keep extraction runnable
    _HAVE_LLM_RESOLUTION = False

    def _resolve_llm_model(explicit=None, override_env=None,
                           require_local_presence=False):
        return explicit or os.environ.get("TRACE_LLM_MODEL") or "qwen2.5:7b"

    def _fallback_model(require_presence=True):
        return os.environ.get("TRACE_LLM_FALLBACK_MODEL", "qwen2.5:7b")


def _local_fallback_model() -> str:
    """Local safety-net model. Presence-checked so we never trigger a silent
    multi-GB Ollama pull (spec v4 section 6.1). Falls back to the plain name only
    when the resolver module is unavailable."""
    if _HAVE_LLM_RESOLUTION:
        try:
            return _fallback_model(require_presence=True)
        except RuntimeError as exc:
            print(f"   [Security] {exc}")
            print("   [Security] refusing to let Ollama start a synchronous pull")
            raise
    return os.environ.get("TRACE_LLM_FALLBACK_MODEL", "qwen2.5:7b")

# PII / secret patterns to scrub before sending text to LLM
PII_PATTERNS = [
    re.compile(r'gh[pousr]_[A-Za-z0-9]{36}'),                      # GitHub PAT
    re.compile(r'sk-[A-Za-z0-9]{20,}'),                            # OpenAI-style keys
    re.compile(r'AIza[A-Za-z0-9_\\-]{35}'),                       # Google API keys
    re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'), # emails
    re.compile(r'(?:password|passwd|pwd|secret|token|api_key|apikey|access_key)\s*[:=]\s*\S+', re.IGNORECASE),
    re.compile(r'Bearer\s+[A-Za-z0-9._\-]+'),                     # Bearer tokens
    re.compile(r'xox[baprs]-[A-Za-z0-9-]+'),                        # Slack tokens
    re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),  # PEM keys
    # Long opaque tokens (JWT, base64 secrets, hex keys) — the "uncommon format" gap.
    re.compile(r'\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b'),  # JWT
    re.compile(r'\b[A-Fa-f0-9]{32,}\b'),                          # hex secrets (>=32)
    re.compile(r'\b[A-Za-z0-9+/]{40,}={0,2}\b'),                  # base64 blobs (>=40)
    re.compile(r'(?:\+33|0)[1-9](?:[\s.\-]?\d{2}){4}'),           # FR phone numbers
    re.compile(r'\b(?:\d[ -]?){13,19}\b'),                        # card-like digit runs
]

def sanitize_pii(text: str) -> str:
    """Best-effort removal of API keys, tokens, emails, passwords, phone numbers
    and long opaque blobs from text BEFORE any LLM submission.

    SECURITY: this is a defence-in-depth filter, NOT a guarantee. Regex scrubbing
    cannot catch every secret in an arbitrary format. The transport decision (local
    vs cloud) is the primary control; see llm_destination() below.
    """
    for pattern in PII_PATTERNS:
        text = pattern.sub('[REDACTED]', text)
    return text


def _find_ollama_api_key_sources() -> tuple[str, str]:
    """Return (source, key) for the first Ollama API key found.

    Mirrors the lookup order of get_ollama_api_key() so the transport disclosure
    cannot disagree with the transport actually used. Source is a short label:
    'env', 'secrets-file', 'config' or '' when no key is available.
    """
    key = os.environ.get("OLLAMA_API_KEY", "").strip()
    if key:
        return ("env", key)
    for secrets_candidate in (
        Path.home() / ".openclaw" / "workspace" / ".secrets" / "ollama.json",
        Path.home() / ".openclaw" / ".secrets" / "ollama.json",
    ):
        try:
            if secrets_candidate.exists():
                d = json.loads(secrets_candidate.read_text())
                v = d.get("apiKey") or d.get("key") or ""
                if isinstance(v, str) and v.strip():
                    return ("secrets-file", v.strip())
        except Exception:
            continue
    try:
        cfg_path = Path(os.environ.get("OPENCLAW_CONFIG", Path.home() / ".openclaw" / "openclaw.json"))
        cfg = json.loads(cfg_path.read_text())
        ak = (cfg.get("models", {}).get("providers", {}).get("ollama", {}) or {}).get("apiKey", "")
        if isinstance(ak, str) and ak.strip():
            return ("config", ak.strip())
        if isinstance(ak, dict):
            sid = ak.get("id") or ak.get("name") or ""
            ref = os.environ.get(sid, "").strip()
            if ref:
                return ("config-store", ref)
    except Exception:
        pass
    return ("", "")


def llm_destination() -> tuple[str, str]:
    """Return (kind, label) describing where extraction text will be sent.

    kind is 'cloud' or 'local'. Used to disclose the transport to the operator
    before any session/memory content leaves the machine.

    SECURITY: this MUST stay in sync with get_ollama_api_key() and the actual
    call path in extract_with_llm(). An earlier version only checked the
    OLLAMA_API_KEY environment variable, so a key sourced from the secrets file
    or openclaw.json made the banner claim "local fallback" while the content
    was in fact posted to ollama.com. The lookup order is now shared.

    CONSENT (v4.0.1): cloud transport is OPT-IN. A configured API key alone is
    no longer enough — the operator must also set TRACE_LLM_ALLOW_CLOUD=1. A
    memory skill that silently ships notes off-machine just because a key
    happens to exist surprises the user; defaulting to local keeps the behaviour
    predictable. TRACE_LLM_LOCAL_ONLY=1 still wins as a hard local-only lock.
    """
    if os.environ.get("TRACE_LLM_LOCAL_ONLY", "").strip() in ("1", "true", "yes"):
        return ("local", "local Ollama (127.0.0.1:11434) — forced by TRACE_LLM_LOCAL_ONLY")
    source, _key = _find_ollama_api_key_sources()
    if source and os.environ.get("TRACE_LLM_ALLOW_CLOUD", "").strip() in ("1", "true", "yes"):
        return ("cloud", f"Ollama cloud (ollama.com) — key from {source} — content leaves this machine")
    if source:
        return ("local", "local Ollama (127.0.0.1:11434) — API key present but cloud not opted in "
                         "(set TRACE_LLM_ALLOW_CLOUD=1 to allow)")
    # No key anywhere: the cloud call is skipped and the local fallback is used.
    return ("local", "local Ollama (127.0.0.1:11434) — no API key configured")


def normalize_date(value, fallback: "str | None" = None) -> "str | None":
    """Return a clean ``YYYY-MM-DD`` string, or ``fallback`` when unparsable.

    This is the single gate every date passes before it is written to the graph
    or folded into an entity id. The date often comes from the LLM, and a model
    asked for ``YYYY-MM-DD`` still returns ``2026-05-31-0913`` (date + time),
    ``2026-05-26-roadmap-updates`` (date + free text) or ``2026-04`` (month
    only). Concatenating those straight into an id produced the garbage nodes
    ``day_202605310913`` / ``day_20260526roadmapupdates`` / ``day_202604`` that
    no edge can ever match -- the dangling-target defect found on 10/10/2026.

    Parse first, build second: a real calendar date is required (``datetime``
    rejects 2026-13-01 and 2026-02-30), and the leading ``YYYY-MM-DD`` of a
    longer string is kept. Anything else falls back (today, at the call site).
    """
    if value is None:
        return fallback
    s = str(value).strip()
    if not s:
        return fallback
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})(?:\b|$)", s)
    if not m:
        return fallback
    try:
        datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return fallback
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"


def stable_id(prefix: str, text: str, date_str: str) -> str:
    """Deterministic entity ID. sha256 is stable across processes (unlike hash()).

    The date is normalised first: an id must never be built by concatenating an
    unvalidated string (see normalize_date). A malformed date becomes today's
    date rather than leaking its digits into the id.
    """
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]
    clean = normalize_date(date_str, date.today().isoformat())
    return f"{prefix}_{clean.replace('-', '')}_{digest}"


WORKSPACE = Path(os.environ.get("WORKSPACE", Path.home() / ".openclaw/workspace"))
ONTOLOGY_FILE = WORKSPACE / "memory" / "ontology" / "graph.jsonl"
DAILY_NOTES_DIR = WORKSPACE / "memory"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
EXTRACTED_FLAG = WORKSPACE / "memory" / ".trace-extracted"
# SECURITY: No global SESSIONS_DIR access — session transcripts may contain
# secrets, private conversations, and unrelated context. Use --session-file
# for explicit, opt-in extraction of a single file.

EXTRACTION_PROMPT = """Analyze the sanitized daily notes below and extract ONLY genuinely significant items.

SECURITY RULES (MANDATORY):
0. NEVER extract credentials, API keys, tokens, passwords, emails, personal data, or session IDs.
1. DECISIONS: Only NEW choices that were MADE (concrete actions taken, not discussed or mentioned)
2. ERRORS: Only real bugs/failures that required a fix or workaround
3. FACTS: Only NEW information (versions, configs, status changes) not already widely known
4. EXCLUDE: routine status ("summary executed", "flag deleted"), warnings without impact, vague mentions
5. EXCLUDE: any casual conversational context, personal opinions, or subjective commentary
6. Be SPECIFIC: include names, versions, numbers (but never secrets)
7. Keep descriptions SHORT (max 15 words each)
8. SUBJECT (M4): every item MUST carry a `subject` — the SHORT entity the item is
   about, lowercased, words joined with underscores (e.g. dovaato, kavita_home,
   backup_cron, astrocapture). Use the same subject for items about the same
   entity, and never invent an entity absent from the note. If truly no entity
   fits, use "general". The subject is what lets the conflict resolver detect
   that a later note contradicts an earlier one.
9. RELATED_TO (M6): every item MUST carry a `related_to` — the id of an EXISTING
   entity this item attaches to (a Project, Person, Service, Skill or Device
   already present in the note's context). An item is not a free-floating fact:
   tie it to what it is about. The id must be lowercase with words joined by
   underscores (e.g. astrocapture, home_assistant, maison_jeanne, kavita).
   It MUST be grounded in the note text — never invented. If genuinely nothing
   fits, use "daily_notes" (the catch-all root). An item with no relation is
   an orphan, and orphans are the graphe's main defect (889/928 on 10/10/2026).

Return ONLY valid JSON. No markdown. No code fences. No extra text. Just the JSON object:
{"decisions":[{"what":"short description","subject":"entity_key","related_to":"existing_entity_id","date":"YYYY-MM-DD"}],"errors":[{"what":"short description","subject":"entity_key","related_to":"existing_entity_id","date":"YYYY-MM-DD"}],"facts":[{"what":"short description","subject":"entity_key","related_to":"existing_entity_id","date":"YYYY-MM-DD"}],"promote_to_memory":["items worth promoting to MEMORY.md"]}

DAILY NOTES:
"""


def extract_session_file(session_path: Path, days_back: int = 3) -> tuple[str, str] | None:
    """Extract conversation text from a single session transcript file.

    SECURITY: Only processes a file explicitly provided via --session-file.
    No global session directory scanning.
    """
    if not session_path.exists():
        print(f"   ⚠️ Session file not found: {session_path}")
        return None

    # Constrain to workspace or explicit absolute path
    resolved = session_path.resolve()
    if not (resolved.is_relative_to(WORKSPACE.resolve()) or session_path.is_absolute()):
        print(f"   ⚠️ Session file outside workspace, skipping: {session_path}")
        return None

    cutoff = datetime.now() - timedelta(days=days_back)
    mtime = datetime.fromtimestamp(session_path.stat().st_mtime)
    if mtime < cutoff:
        print(f"   ⚠️ Session file older than {days_back} days, skipping")
        return None

    texts = []
    try:
        with open(session_path) as fh:
            for line in fh:
                try:
                    entry = json.loads(line.strip())
                except json.JSONDecodeError:
                    continue

                if entry.get("type") != "message":
                    continue

                msg = entry.get("message", {})
                role = msg.get("role", "")
                content = msg.get("content", "")

                # Skip tool results (too noisy)
                if role == "toolResult":
                    continue

                # Extract text from content blocks or string
                if isinstance(content, list):
                    text_parts = []
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            t = block.get("text", "")
                            # Skip heartbeat/empty messages
                            if t and t.strip() not in ("HEARTBEAT_OK", "NO_REPLY", "[OpenClaw heartbeat poll]") and len(t) > 20:
                                text_parts.append(t)
                    if text_parts:
                        combined = ' '.join(text_parts)
                        if len(combined) > 30:
                            texts.append(f"{role}: {combined[:500]}")
                elif isinstance(content, str) and len(content) > 20:
                    if content.strip() not in ("HEARTBEAT_OK", "NO_REPLY", "[OpenClaw heartbeat poll]"):
                        texts.append(f"{role}: {content[:500]}")
    except Exception as e:
        print(f"   ⚠️ Error reading {session_path.name}: {e}")
        return None

    if not texts:
        return None

    session_text = "\n".join(texts)
    # Truncate to max 4000 chars for LLM
    if len(session_text) > 4000:
        session_text = session_text[-4000:]
        session_text = session_text[session_text.index('\n') + 1:]

    return (mtime.strftime("%Y-%m-%d"), session_text)


def load_ontology_ids():
    """Load existing entity IDs from ontology."""
    ids = set()
    if ONTOLOGY_FILE.exists():
        for line in ONTOLOGY_FILE.read_text().strip().split("\n"):
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
                eid = entry.get("entity", {}).get("id", "")
                if eid:
                    ids.add(eid)
            except json.JSONDecodeError:
                continue
    return ids


def load_memory_content():
    """Load MEMORY.md for dedup check."""
    if MEMORY_FILE.exists():
        return MEMORY_FILE.read_text().lower()
    return ""


def load_extracted_sessions():
    """Load set of already-extracted dates."""
    if EXTRACTED_FLAG.exists():
        return set(EXTRACTED_FLAG.read_text().strip().split("\n"))
    return set()


def save_extracted_date(day_str):
    """Mark a date as extracted."""
    sessions = load_extracted_sessions()
    sessions.add(day_str)
    EXTRACTED_FLAG.write_text("\n".join(sorted(sessions)) + "\n")


def extract_with_llm(text, dry_run=False):
    """Use LLM (Ollama cloud primary, Ollama local fallback) to extract structured info.

    SECURITY / DISCLOSURE: memory and session content IS transmitted to an LLM.
      - Primary transport is Ollama cloud (https://ollama.com) ONLY when an API key
        is configured AND the operator sets TRACE_LLM_ALLOW_CLOUD=1: content LEAVES
        this machine (opt-in, v4.0.1).
      - Otherwise: local Ollama at 127.0.0.1:11434, content stays on the machine.
      - Set TRACE_LLM_LOCAL_ONLY=1 to force local-only and refuse cloud calls even
        when cloud was opted in (hard lock).
    Text is sanitized (sanitize_pii) before submission, but regex scrubbing is
    best-effort, NOT a guarantee. Do not feed raw secret material to this function.
    """
    import urllib.request
    import urllib.error
    import time

    # Sanitize PII/secrets before any LLM submission
    text = sanitize_pii(text)

    # Truncate to avoid timeout/context limits
    MAX_CHARS = 8000
    if len(text) > MAX_CHARS:
        text = text[-MAX_CHARS:]
        text = text[text.index('\n') + 1:]

    prompt = EXTRACTION_PROMPT + text

    kind, label = llm_destination()
    if not dry_run:
        if kind == "cloud":
            print(f"   [Security] ⚠️  CLOUD TRANSMISSION: sending sanitized excerpt to {label}")
        else:
            print(f"   [Security] Sending sanitized excerpt to {label} (stays on this machine)")

    def parse_llm_output(output):
        """Extract JSON from LLM output, fixing common issues.

        Handles: markdown fences, trailing commas, single quotes, and
        TRUNCATED output (done_reason=length) by salvaging the largest
        valid JSON prefix and closing open brackets.
        """
        if not output or not output.strip():
            return None
        json_match = re.search(r'\{[\s\S]*\}', output)
        json_str = json_match.group() if json_match else None

        def _try(s):
            s = re.sub(r',\s*([}\]])', r'\1', s)
            s = re.sub(r'^```json\s*', '', s)
            s = re.sub(r'\s*```$', '', s)
            try:
                return json.loads(s)
            except json.JSONDecodeError:
                try:
                    return json.loads(s.replace("'", '"'))
                except json.JSONDecodeError:
                    return None

        if json_str is not None:
            parsed = _try(json_str)
            if parsed is not None:
                return parsed

        # Truncation salvage (STRICT): keep only FULLY-PARSED elements that
        # appear before the cut. If an object is incomplete, drop it entirely
        # rather than keep an amputated value — a truncated fact is worse than
        # no fact in long-term memory. Never invents content.
        start = output.find('{')
        if start < 0:
            return None
        frag = output[start:]
        # Cut at the last top-level-friendly boundary: last comma that is NOT
        # inside an unterminated string. Simpler robust approach: repeatedly
        # trim the tail until the fragment closes cleanly or we run out.
        candidates = []
        # Try dropping progressively from the last comma backwards.
        idx = len(frag)
        while True:
            cut = frag.rfind(',', 0, idx)
            if cut < 0:
                break
            cand = frag[:cut]
            dc = cand.count('{') - cand.count('}')
            ds = cand.count('[') - cand.count(']')
            if cand.count('"') % 2 == 0 and dc >= 0 and ds >= 0:
                closed = cand + ']' * ds + '}' * dc
                p = _try(closed)
                if p is not None:
                    print("   ♻️  Salvaged strict partial JSON (dropped incomplete trailing element)")
                    return p
            idx = cut
        return None

    def get_ollama_api_key():
        """Get Ollama API key, in order of precedence:
        1. env var OLLAMA_API_KEY (injected by OpenClaw automation runtime)
        2. dedicated secrets file ~/.openclaw/workspace/.secrets/ollama.json
        3. openclaw.json provider config (resolving store references if possible)
        If no plaintext key is found, returns empty string (caller will report it).

        SECURITY: keep the lookup order identical to _find_ollama_api_key_sources()
        so the disclosure in llm_destination() matches the transport actually used.
        """
        return _find_ollama_api_key_sources()[1]

    def call_ollama_cloud(attempt):
        """Call Ollama cloud API (ollama.com). Returns raw content or None.

        REFUSES to run when TRACE_LLM_LOCAL_ONLY is set: the local-only mode must
        not silently fall back to a transport that leaves the machine.

        CONSENT (v4.0.1): cloud is opt-in. Even with an API key present, the call
        is refused unless TRACE_LLM_ALLOW_CLOUD=1 — so a stray key in the
        environment can never ship memory content off-machine on its own.
        """
        if os.environ.get("TRACE_LLM_LOCAL_ONLY", "").strip() in ("1", "true", "yes"):
            print("   [Security] TRACE_LLM_LOCAL_ONLY=1 — cloud call refused (local-only mode)")
            return None
        if os.environ.get("TRACE_LLM_ALLOW_CLOUD", "").strip() not in ("1", "true", "yes"):
            print("   [Security] TRACE_LLM_ALLOW_CLOUD not set — cloud call refused (local by default)")
            return None
        api_key = get_ollama_api_key()
        if not api_key:
            print("   ⚠️ No Ollama API key available")
            return None
        payload = json.dumps({
            "model": os.environ.get("TRACE_LLM_MODEL") or _resolve_llm_model(),
            "messages": [
                {"role": "system", "content": "You extract structured information from daily notes. Respond ONLY with valid JSON."},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "options": {"temperature": 0.1, "num_predict": int(os.environ.get("TRACE_LLM_MAX_TOKENS", "16000"))},
        }).encode('utf-8')
        req = urllib.request.Request(
            "https://ollama.com/api/chat",
            data=payload,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        )
        timeout = 120 + (attempt * 30)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            content = result.get("message", {}).get("content", "")
            done_reason = result.get("done_reason", "")
            if done_reason == "length":
                print("   ⚠️ Ollama cloud: response TRUNCATED (done_reason=length) — output hit num_predict cap")
            return content

    def call_ollama(attempt):
        """Call the local Ollama fallback. Returns raw content or None."""
        model = os.environ.get("TRACE_LLM_FALLBACK_MODEL") or _local_fallback_model()
        payload = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": 0.1, "num_predict": 2048}
        }).encode('utf-8')
        req = urllib.request.Request(
            "http://127.0.0.1:11434/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        timeout = 90 + (attempt * 30)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            return result.get("message", {}).get("content", "")

    # Primary: Ollama cloud (2 retries) — rattrapage sur réponse tronquée/absente.
    # (1 seul essai laissait passer les coupures ; 3 faisaient perdre ~6 min.
    #  Un retry au 1er échec suffit à rattraper une troncature, coût faible.)
    for attempt in range(2):
        try:
            output = call_ollama_cloud(attempt)
            if output and output.strip():
                parsed = parse_llm_output(output)
                if parsed is not None:
                    return parsed
                print(f"   ⚠️ JSON parse failed (attempt {attempt+1}/2)")
            else:
                print(f"   ⚠️ Empty Ollama response (attempt {attempt+1}/2)")
        except Exception as e:
            print(f"   ⚠️ Ollama API error: {e} (attempt {attempt+1}/2)")
        if attempt == 0:
            time.sleep(1)

    # Fallback: Ollama local
    print("   ⚠️ Ollama cloud failed, falling back to local Ollama (qwen2.5:7b)...")
    for attempt in range(2):
        try:
            output = call_ollama(attempt)
            if output and output.strip():
                parsed = parse_llm_output(output)
                if parsed is not None:
                    return parsed
        except Exception as e:
            print(f"   ⚠️ Ollama error: {e} (attempt {attempt+1}/2)")
        time.sleep(2 ** attempt)

    print("   ⚠️ LLM extraction failed after all attempts")
    return None


def extract_with_patterns(text):
    """Fallback: pattern-based extraction (less accurate)."""
    decisions = []
    errors = []
    facts = []
    
    # Routine markers to EXCLUDE (not real facts)
    routine_patterns = [
        r'morning summary exécuté', r'blogwatcher read-all', r'flag.*supprimé',
        r'telegram envoyé', r'résumé.*envoyé', r'veille-trigger',
        r'leadership.*→ supabase', r'spanish.*envoyé', r'reading.*vérifié',
        r'med.*doses restantes', r'astro weather.*\d+/100',
        r'blogwatcher.*\d+ nouveaux articles$',
        r'^-\s+.*due\s+\d', r'^-\s+.*\(due ',  # overdue task lines
        r'heartbeat poll', r'HEARTBEAT_OK', r'NO_REPLY',
    ]
    
    # Check if a line is routine noise
    def is_routine(line):
        line_lower = line.lower()
        return any(re.search(p, line_lower) for p in routine_patterns)
    
    for line in text.split("\n"):
        line_stripped = line.strip()
        if not line_stripped or len(line_stripped) < 20:
            continue
        # Skip lines that are conversation role prefixes from session transcripts
        if line_stripped.startswith('user:') or line_stripped.startswith('assistant:'):
            content_after_role = re.sub(r'^(user|assistant):\s*', '', line_stripped)
            if len(content_after_role) < 30 or is_routine(content_after_role):
                continue
        if is_routine(line_stripped):
            continue
        
        # Errors: ⚠️ or ❌ markers with real content
        if "⚠️" in line or "❌" in line:
            clean = re.sub(r'^[- ]*❌\s*', '', line_stripped)
            clean = re.sub(r'^[- ]*⚠️\s*', '', clean)
            # Skip routine warnings and overdue task lines
            if not is_routine(clean) and len(clean) > 25 and 'due' not in clean.lower()[:20]:
                errors.append(clean[:200])
        
        # Explicit decision markers: - ✅ + decisive verbs
        if line_stripped.startswith("- ✅") or line_stripped.startswith("✅"):
            clean = re.sub(r'^[- ]*✅\s*', '', line_stripped)
            # Only if it contains a decision verb
            decision_verbs = ['décidé', 'choisi', 'chose', 'choix', 'configured', 'migrated', 
                            'installé', 'créé', 'ajouté', 'switched', 'supprimé', 'retiré',
                            'remplacé', 'fixed', 'corrigé', 'résolu']
            if any(v in clean.lower() for v in decision_verbs) and not is_routine(clean):
                decisions.append(clean[:200])
        
        # Version/status changes: lines with version numbers or specific configs
        version_match = re.search(r'(?:v\d+\.\d+|version\s*[:\-]?\s*\S+|port\s+\d{4})', line_stripped.lower())
        if version_match and not is_routine(line_stripped) and len(line_stripped) > 30:
            facts.append(line_stripped[:200])
    
    # Deduplicate
    decisions = list(dict.fromkeys(decisions))[:5]
    errors = list(dict.fromkeys(errors))[:5]
    facts = list(dict.fromkeys(facts))[:5]
    
    return {
        "decisions": [{"what": d, "date": date.today().isoformat()} for d in decisions],
        "errors": [{"what": e, "date": date.today().isoformat()} for e in errors],
        "facts": [{"what": f, "date": date.today().isoformat()} for f in facts],
        "patterns": [],
        "promote_to_memory": []
    }


def _norm_subject(item) -> "str | None":
    """Normalise an extracted item's subject the SAME way auto_capture.py does.

    M4: trace_extractor.py used to carry no subject at all, so every trace item
    reached the fact ledger with subject=NULL and the conflict resolver could not
    match a later note against an earlier one (arbitration returned
    "no confident relation detected" for everything). We reuse the exact
    normalisation rules of auto_capture._normalise_facts so both producers agree
    on the key: lowercase, words -> underscores, grounded against the text,
    never invented. A subject that grounds nothing is dropped.
    """
    if not isinstance(item, dict):
        return None
    what = str(item.get("what") or item.get("content") or "").strip()
    subject = str(item.get("subject") or "").strip().lower()
    subject = re.sub(r"\s+", "_", subject) or None
    if not subject:
        return None
    # The LLM is asked for snake_case ("kavita_home"), and '\w' INCLUDES '_', so
    # splitting on '[^\w]+' left the key in ONE token and grounding then failed,
    # collapsing "kavita_home" to the fallback word "kavita". Split on underscore
    # too, so each entity word can be grounded independently.
    tokens = [t for t in re.split(r"[^\w]+", subject.replace("_", " ")) if len(t) >= 3]
    # Compare against the TOKENISED text, never the space-stripped string:
    # "kavita home" flattened to "kavitahome" makes "home" unmatchable, which
    # silently truncated the key (M4 root cause carried over from auto_capture).
    text_words = set(re.findall(r"[\w\u00c0-\u00ff]+", what.lower()))
    grounded = [t for t in tokens if t in text_words]
    if grounded:
        return "_".join(grounded[:2])
    if tokens:
        words = [w.lower() for w in re.findall(r"[A-Za-z\u00c0-\u00ff]{4,}", what)]
        return words[0] if words else None
    return None


def write_daily_extraction(extractions, source="trace-extractor"):
    """Write extracted items to today's daily notes."""
    today = date.today().isoformat()
    daily_file = DAILY_NOTES_DIR / f"{today}.md"
    
    # Check if already extracted today
    if daily_file.exists():
        content = daily_file.read_text()
        if "[trace-extractor]" in content:
            return False
    
    entry = f"\n## [{source}] {datetime.now().strftime('%H:%M')} — Auto-extracted trace items"
    
    for category, label, emoji in [
        ("decisions", "Decisions", "🟢"),
        ("errors", "Errors", "🔴"),
        ("facts", "New facts", "🔵"),
        ("patterns", "Patterns", "🟡"),
    ]:
        items = extractions.get(category, [])
        if items:
            entry += f"\n**{label}:**"
            for item in items:
                what = item.get("what", item) if isinstance(item, dict) else item
                subj = _norm_subject(item) if isinstance(item, dict) else None
                # M4: carry the entity key into the note line so the downstream
                # indexer can attach a real subject instead of NULL.
                tag = f" [subject:{subj}]" if subj else ""
                entry += f"\n- {emoji} {what}{tag}"
    
    promotions = extractions.get("promote_to_memory", [])
    if promotions:
        entry += "\n**⬆️ Promote to MEMORY.md:**"
        for p in promotions:
            entry += f"\n- {p}"
    
    if daily_file.exists():
        content = daily_file.read_text()
        daily_file.write_text(content.rstrip() + entry + "\n")
    else:
        daily_file.write_text(entry + "\n")
    
    return True



def upsert_entities(records):
    """Physically upsert records into the ontology file.

    The file is an OP-log (one JSON object per line). A true upsert means:
    read the current state, replace matching entities in place, append the new
    ones. It rewrites the whole file, which is acceptable at this size
    (a few hundred KB) and keeps the file compact between GC runs.

    Uses a fresh read of existing IDs (never a stale in-memory cache).
    """
    if not records:
        return 0

    incoming = {}
    for rec in records:
        eid = rec.get("entity", {}).get("id")
        if eid:
            incoming[eid] = rec

    if not incoming:
        return 0

    lines = []
    written = set()
    if ONTOLOGY_FILE.exists():
        for line in ONTOLOGY_FILE.read_text().splitlines():
            if not line.strip():
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                lines.append(line)
                continue
            eid = entry.get("entity", {}).get("id")
            if eid and eid in incoming:
                lines.append(json.dumps(incoming[eid], ensure_ascii=False))
                written.add(eid)
            else:
                lines.append(line)

    for eid, rec in incoming.items():
        if eid not in written:
            lines.append(json.dumps(rec, ensure_ascii=False))

    tmp = ONTOLOGY_FILE.with_suffix(".jsonl.tmp")
    tmp.write_text("\n".join(lines) + "\n")
    tmp.replace(ONTOLOGY_FILE)
    return len(incoming)

def _norm_related_to(item) -> "str | None":
    """Normalise an extracted item's `related_to` into a candidate root id.

    M6: the extraction prompt now requires a `related_to` — the id of an existing
    entity the item attaches to. Without this, every extracted fact becomes an
    orphan (889/928 on 10/10/2026). We normalise the same way as the subject
    (lowercase, words -> underscores) and REQUIRE it to be grounded in the item
    text, so the LLM cannot invent a root that does not exist in the note.
    Returns None when nothing grounds.
    """
    if not isinstance(item, dict):
        return None
    raw = str(item.get("related_to") or "").strip().lower()
    if not raw:
        return None
    raw = re.sub(r"[^a-z0-9_]+_", "_", re.sub(r"\s+", "_", raw)).strip("_")
    what = str(item.get("what") or item.get("content") or "").strip().lower()
    if not what:
        return None
    tokens = [t for t in re.split(r"[^\w]+", raw.replace("_", " ")) if len(t) >= 3]
    text_words = set(re.findall(r"[\w\u00c0-\u00ff]+", what.lower())) | set(
        re.findall(r"[\w\u00c0-\u00ff]+", str(item.get("subject") or "").lower()))
    grounded = [t for t in tokens if t in text_words]
    if grounded:
        return "_".join(grounded[:2])
    # Not grounded in the item text -> do not invent a root.
    return None


def _root_id_for(item, existing_ids) -> "str | None":
    """Resolve the root an item should attach to.

    Order: the extracted `related_to` (if it names a KNOWN entity), the subject
    (same rule), then None. Never returns an id absent from the ontology unless
    it is the explicit catch-all, which write_ontology_entities() will create.
    """
    for key in ("related_to", "subject"):
        cand = _norm_related_to({"related_to": item.get(key), "what": item.get("what"),
                                 "subject": item.get("subject")}) if key == "related_to" \
               else _norm_subject(item)
        if cand and cand in existing_ids:
            return cand
    return None


def write_ontology_entities(extractions):
    """Add new entities to ontology from extractions, using upsert to avoid duplicates.

    M6: each decision is ALSO attached to a root entity via a ``relate`` fact, so
    it never lands as an orphan. The root comes from the extracted ``related_to``
    (grounded against the item text) or the ``subject``; when neither names a
    known entity we fall back to the catch-all root ``daily_notes``, which is
    created on first use. A node without an edge is the graphe's main defect.
    """
    existing_ids = load_ontology_ids()
    new_entities = []
    new_relations = []

    # Ensure the catch-all root exists so a fallback link is always possible.
    CATCH_ALL = "daily_notes"
    if CATCH_ALL not in existing_ids:
        new_entities.append({
            "op": "upsert",
            "entity": {
                "id": CATCH_ALL,
                "type": "Concept",
                "properties": {
                    "name": "Daily notes (catch-all root)",
                    "description": "Root for extracted facts with no better anchor.",
                    "source": "trace-extraction",
                },
            },
        })
        existing_ids.add(CATCH_ALL)

    for dec in extractions.get("decisions", []):
        what = dec.get("what", "") if isinstance(dec, dict) else dec
        # Create a clean ID from the decision
        entity_id = stable_id("dec", what, date.today().isoformat())
        if entity_id not in existing_ids:
            new_entities.append({
                "op": "upsert",
                "entity": {
                    "id": entity_id,
                    "type": "Decision",
                    "properties": {
                        "description": what[:200],
                        # The LLM's date is untrusted: normalise before it reaches the
                        # graph. A malformed value ("2026-05-31-0913") otherwise
                        # becomes an unmatchable node/edge target later. Falls back
                        # to today, which is the honest answer for "undated decision".
                        "date": normalize_date(dec.get("date"), date.today().isoformat()),
                        "source": "trace-extraction"
                    }
                }
            })
            existing_ids.add(entity_id)
        # Attach to a root (never leave the decision orphaned).
        if isinstance(dec, dict):
            root = _root_id_for(dec, existing_ids) or CATCH_ALL
            new_relations.append({
                "op": "relate", "from": entity_id, "rel": "relates_to", "to": root,
                "properties": {
                    "evidence": "auto-link at extraction (M6 related_to contract)",
                    "source": "trace-extraction",
                    "valid_from": date.today().isoformat(),
                },
            })

    if new_entities:
        upsert_entities(new_entities)
    if new_relations:
        _append_relations(new_relations)

    return len(new_entities)


def _append_relations(relations):
    """Append ``relate`` facts to the ontology log. Never rewrites or deletes."""
    if not relations:
        return 0
    with ONTOLOGY_FILE.open("a", encoding="utf-8") as fh:
        for rel in relations:
            fh.write(json.dumps(rel, ensure_ascii=False, sort_keys=True) + "\n")
    return len(relations)


def write_timeline_events(extractions):
    """Create TimelineEvent entities from extractions."""
    existing_ids = load_ontology_ids()
    today = date.today().isoformat()
    new_events = []
    
    # Map extraction categories to timeline categories
    category_map = {
        "decisions": "work",
        "errors": "technical",
        "facts": "technical",
        "patterns": "technical",
    }
    
    for ext_cat, items in extractions.items():
        if ext_cat not in category_map:
            continue
        tl_category = category_map[ext_cat]
        
        for item in items:
            what = item.get("what", item) if isinstance(item, dict) else item
            if not what or len(what) < 10:
                continue
            
            # Deterministic ID (sha256, stable across processes)
            eid = stable_id("tl", what, today)
            
            if eid in existing_ids:
                continue
            
            entity = {
                "op": "create",
                "entity": {
                    "id": eid,
                    "type": "TimelineEvent",
                    "properties": {
                        "date": today,
                        "description": what[:200],
                        "category": tl_category,
                        "source": "trace-extraction"
                    }
                }
            }
            new_events.append(entity)
            existing_ids.add(eid)
    
    if new_events:
        for e in new_events:
            e["op"] = "upsert"
        upsert_entities(new_events)
    
    return len(new_events)


def auto_promote_to_memory(promotions):
    """Auto-promote items to MEMORY.md if not already there."""
    if not promotions:
        return 0
    
    memory_content = MEMORY_FILE.read_text() if MEMORY_FILE.exists() else ""
    promoted = []
    
    # Find the Active Decisions section
    lines = memory_content.split('\n')
    decisions_idx = None
    for i, line in enumerate(lines):
        if '## Active Decisions' in line:
            decisions_idx = i
            break
    
    if decisions_idx is None:
        # No Active Decisions section found, skip
        return 0
    
    for item in promotions:
        # Check if already in MEMORY.md
        key_terms = [w for w in item.lower().split() if len(w) > 4]
        if all(term in memory_content.lower() for term in key_terms[:3]):
            continue
        
        # Add as a new line after the decisions header
        # Format: - **Item** (date)
        today = date.today().isoformat()
        new_line = f"- **{item}** ({today})"
        lines.insert(decisions_idx + 1, new_line)
        promoted.append(item)
    
    if promoted:
        MEMORY_FILE.write_text('\n'.join(lines))
    
    return len(promoted)


def check_promotions(extractions):
    """Check what should be promoted to MEMORY.md."""
    memory_content = load_memory_content()
    promotions = []
    
    for item in extractions.get("promote_to_memory", []):
        # Check if already in MEMORY.md
        key_terms = [w for w in item.lower().split() if len(w) > 4]
        if not all(term in memory_content for term in key_terms[:3]):
            promotions.append(item)
    
    return promotions


def main():
    parser = argparse.ArgumentParser(description="Extract traces from daily notes and sessions (v2 - LLM-powered)")
    parser.add_argument("--all", action="store_true", help="Process all unprocessed dates")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--days", type=int, default=3, help="Number of recent days to process (default: 3)")
    parser.add_argument("--llm", action="store_true", help="Use LLM for extraction (default: pattern-based)")
    parser.add_argument("--session-file", type=str, default=None,
                        help="Extract from a single session transcript file (explicit opt-in). "
                             "Path must be absolute or relative to workspace.")
    parser.add_argument("--date", type=str, help="Process specific date (YYYY-MM-DD)")
    args = parser.parse_args()
    
    print("🔍 Trace Extractor v2 — LLM-powered extraction")
    print("=" * 55)
    
    # Collect daily notes
    notes = []
    extracted = load_extracted_sessions()
    
    if args.date:
        f = DAILY_NOTES_DIR / f"{args.date}.md"
        if f.exists():
            notes.append((args.date, f.read_text()))
    else:
        for i in range(args.days):
            d = (date.today() - timedelta(days=i)).isoformat()
            f = DAILY_NOTES_DIR / f"{d}.md"
            if f.exists() and d not in extracted:
                notes.append((d, f.read_text()))
    
    # Also collect session transcript if explicitly provided
    session_texts = []
    if args.session_file:
        print("📋 Extracting from session file...")
        session_path = Path(args.session_file)
        result = extract_session_file(session_path, days_back=args.days)
        if result:
            day, text = result
            print(f"   Session: {session_path.name[:40]}... ({len(text)} chars)")
            session_texts = [(day, text)]
        else:
            print("   ⚠️ No extractable content from session file")
    
    if not notes and not session_texts:
        print("No unprocessed daily notes or sessions found.")
        return
    
    print(f"📄 Processing {len(notes)} daily notes" + (f" + {len(session_texts)} sessions" if session_texts else ""))
    
    # Extract
    all_extractions = {"decisions": [], "errors": [], "facts": [], "patterns": [], "promote_to_memory": []}
    
    def merge_extractions(target, source):
        for key in target:
            if key in source:
                target[key].extend(source[key])
    
    # Process daily notes
    if args.llm and notes:
        print("🤖 Using LLM extraction (per-day)...")
        for day_str, day_text in notes:
            print(f"   Processing notes {day_str}...")
            result = extract_with_llm(day_text, dry_run=args.dry_run)
            if result:
                merge_extractions(all_extractions, result)
            else:
                print(f"   ⚠️ LLM failed for {day_str}, using pattern fallback")
                pattern_result = extract_with_patterns(day_text)
                merge_extractions(all_extractions, pattern_result)
    elif notes:
        print("📐 Using pattern-based extraction for notes...")
        combined_text = "\n".join(text for _, text in notes)
        pattern_result = extract_with_patterns(combined_text)
        merge_extractions(all_extractions, pattern_result)
    
    # Process session transcripts
    if session_texts:
        print("🤖 Extracting from session transcripts...")
        for day_str, text in session_texts:
            # Truncate large sessions
            if len(text) > 6000:
                text = text[-6000:]
                text = text[text.index('\n') + 1:]
            print(f"   Processing session from {day_str} ({len(text)} chars)...")
            if args.llm:
                result = extract_with_llm(text, dry_run=args.dry_run)
                if result:
                    merge_extractions(all_extractions, result)
                else:
                    print(f"   ⚠️ LLM failed for session, using pattern fallback")
                    pattern_result = extract_with_patterns(text)
                    merge_extractions(all_extractions, pattern_result)
            else:
                pattern_result = extract_with_patterns(text)
                merge_extractions(all_extractions, pattern_result)
    
    extractions = all_extractions
    
    # Display results
    for category, label, emoji in [
        ("decisions", "Decisions", "🟢"),
        ("errors", "Errors", "🔴"),
        ("facts", "New facts", "🔵"),
        ("patterns", "Patterns", "🟡"),
    ]:
        items = extractions.get(category, [])
        if items:
            print(f"\n{emoji} {label} ({len(items)}):")
            for item in items:
                what = item.get("what", item) if isinstance(item, dict) else item
                print(f"   • {what[:100]}")
    
    promotions = check_promotions(extractions)
    if promotions:
        print(f"\n⬆️  Promote to MEMORY.md ({len(promotions)}):")
        for p in promotions:
            print(f"   • {p[:100]}")
    
    if args.dry_run:
        print("\n🏁 Dry run — no changes written.")
        return
    
    # Write
    wrote_daily = write_daily_extraction(extractions)
    wrote_ontology = write_ontology_entities(extractions)
    wrote_timeline = write_timeline_events(extractions)
    
    for d, _ in notes:
        save_extracted_date(d)
    
    print(f"\n✅ Written: daily notes {'updated' if wrote_daily else 'skipped'}, {wrote_ontology} ontology entities, {wrote_timeline} timeline events")
    
    if promotions:
        print("\n💡 Review these promotions and add to MEMORY.md if needed.")


if __name__ == "__main__":
    main()