#!/usr/bin/env python3
"""
ghostprint — LLM fingerprint noise injector
Provider-agnostic, zero-dependency, schedule-aware.

Usage:
    python3 ghostprint.py               # run with jitter (cron mode)
    python3 ghostprint.py --run-once    # fire immediately, no jitter
    python3 ghostprint.py --install-cron
    python3 ghostprint.py --stats
"""

import argparse
import json
import os
import re
import secrets
import shlex
import ssl
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────

BASE_DIR    = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.yaml"
LOG_FILE    = BASE_DIR / "ghostprint.log"
TOPICS_FILE = BASE_DIR / "topics.txt"

# ── Cryptographic randomness (replaces stdlib random) ────────────────────────

def _randint(a: int, b: int) -> int:
    """Inclusive random integer [a, b] using CSPRNG."""
    return a + secrets.randbelow(b - a + 1)

def _choice(seq: list):
    """Random element from seq using CSPRNG."""
    return seq[secrets.randbelow(len(seq))]

def _sample(seq: list, k: int) -> list:
    """Random sample of k elements from seq using CSPRNG (Fisher-Yates)."""
    copy = list(seq)
    for i in range(len(copy) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        copy[i], copy[j] = copy[j], copy[i]
    return copy[:k]

def _weighted_choices(population: list, weights: list, k: int) -> list:
    """Weighted random selection of k elements using CSPRNG."""
    total = sum(weights)
    result = []
    for _ in range(k):
        r = int.from_bytes(secrets.token_bytes(4), 'big') / 0x100000000 * total
        acc = 0
        for i, w in enumerate(weights):
            acc += w
            if r <= acc:
                result.append(population[i])
                break
    return result

def _uniform(a: float, b: float) -> float:
    """Uniform float in [a, b) using CSPRNG."""
    return a + (int.from_bytes(secrets.token_bytes(4), 'big') / 0x100000000) * (b - a)


# ── URL validation ───────────────────────────────────────────────────────────

import ipaddress
from urllib.parse import urlparse

_ALLOWED_SCHEMES = {"https"}

def _validate_provider_url(url: str) -> None:
    """Reject non-HTTPS URLs and URLs pointing to private/reserved IPs."""
    parsed = urlparse(url)
    if parsed.scheme not in _ALLOWED_SCHEMES:
        raise ValueError(f"Rejected non-HTTPS base_url: {url}")
    hostname = parsed.hostname or ""
    try:
        addr = ipaddress.ip_address(hostname)
        if addr.is_private or addr.is_reserved or addr.is_loopback or addr.is_link_local:
            raise ValueError(f"Rejected private/reserved IP in base_url: {url}")
    except ValueError as e:
        if "Rejected" in str(e):
            raise
        # hostname is a domain name, not an IP — that's fine


# ── Built-in topics (used if topics.txt absent) ───────────────────────────────

BUILTIN_TOPICS = [
    "What's the best way to store fresh herbs?",
    "How do I remove a stripped screw?",
    "What causes hiccups?",
    "How long does pasta dough last in the fridge?",
    "What's the difference between a virus and bacteria?",
    "Why does the sky turn red at sunset?",
    "How do I clean a cast iron pan?",
    "What's a good substitute for buttermilk in baking?",
    "Why do cats purr?",
    "How do I fix a squeaky door hinge?",
    "What's the best way to remove a wine stain?",
    "How long should I steep green tea?",
    "What causes déjà vu?",
    "How do you fold a fitted sheet neatly?",
    "Why does bread go stale?",
    "What's the difference between jam and jelly?",
    "How do I get rid of fruit flies in the kitchen?",
    "What causes static electricity?",
    "How do I soften hard brown sugar?",
    "What's the fastest way to cool down a hot drink?",
    "Why do onions make you cry?",
    "How do I descale an electric kettle?",
    "What's the best way to ripen an avocado quickly?",
    "How do I stop a minor nosebleed?",
    "Why does metal feel colder than wood at room temperature?",
    "How do I keep cut flowers fresh longer?",
    "What's the difference between baking soda and baking powder?",
    "How do I get rid of a headache without medication?",
    "What causes thunder?",
    "How do I make my coffee less bitter?",
    "How do I keep bananas from turning brown?",
    "What's the difference between perfume and eau de toilette?",
    "How do I unclog a slow drain?",
    "Why do leaves change color in autumn?",
    "How do I get wax out of a candle holder?",
    "What causes muscle cramps?",
    "How do I keep lettuce crisp in the fridge?",
    "What's the best way to clean a wooden cutting board?",
    "How do I sharpen kitchen knives at home?",
    "Why does popcorn pop?",
    "How do I remove a splinter safely?",
    "What causes food cravings?",
    "How do I fix a running toilet?",
    "What's the best way to fold a t-shirt to save space?",
    "Why do we get brain freeze from cold food?",
    "How do I stop cut apples from going brown?",
    "What's the difference between a cold and the flu?",
    "How do I get rid of condensation on windows?",
    "Why does hot water sometimes freeze faster than cold?",
    "How do I make rice not stick to the pot?",
]


# ── Minimal YAML parser (no deps) ────────────────────────────────────────────

def parse_yaml(text: str) -> dict:
    """
    Parse a minimal subset of YAML sufficient for our config.
    Handles: strings, numbers, booleans, nested mappings, lists of dicts.
    Expands ${ENV_VAR} references safely (handles URLs and ${VAR} in values).
    """

    def resolve(val: str) -> str:
        def _expand(m):
            name = m.group(1)
            value = os.environ.get(name)
            if value is None:
                print(f"  ⚠  WARNING: ${{{name}}} is not set in environment")
                return ''
            return value
        return re.sub(r'\$\{(\w+)\}', _expand, val)

    def parse_value(s: str):
        s = s.strip().strip('"').strip("'")
        if s.lower() == 'true':  return True
        if s.lower() == 'false': return False
        try: return int(s)
        except ValueError: pass
        try: return float(s)
        except ValueError: pass
        return resolve(s)

    def safe_kv(content: str):
        """Split 'key: value' safely — key is always a simple identifier."""
        m = re.match(r'^([A-Za-z0-9_\-]+)\s*:\s*(.*)', content)
        return (m.group(1), m.group(2).strip()) if m else (None, None)

    lines = text.splitlines()
    root  = {}

    # Stack entries: (indent_level, container)
    # container is either a dict or a list
    stack = [(0, root)]

    i = 0
    while i < len(lines):
        raw  = lines[i]
        line = raw.rstrip()
        if not line or line.lstrip().startswith('#'):
            i += 1
            continue

        indent  = len(raw) - len(raw.lstrip())
        content = line.strip()

        # ── List item: "- key: val" or just "-" ──────────────────────────────
        if content.startswith('- '):
            item_str = content[2:].strip()

            # Pop to the level that owns this list
            while len(stack) > 1 and stack[-1][0] > indent:
                stack.pop()

            parent = stack[-1][1]

            # parent must be a list — if it's a dict, find the last list value
            if isinstance(parent, dict):
                # Shouldn't normally happen in well-formed YAML, but be safe
                i += 1
                continue

            # Create a new dict for this list item
            obj = {}
            parent.append(obj)

            # Parse inline key: value if present
            if item_str:
                k, v = safe_kv(item_str)
                if k:
                    obj[k] = parse_value(v) if v else None

            # Push this obj so subsequent indented lines go into it
            stack.append((indent + 2, obj))
            i += 1
            continue

        # ── Key: value (or key: <nothing> for mapping/list start) ────────────
        key, val = safe_kv(content)
        if key is None:
            i += 1
            continue

        # Pop stack to the right level: find the nearest container
        # whose indent is LESS THAN current indent (strictly less — not equal).
        # Using >= would pop the dict that was just pushed for this same indent.
        while len(stack) > 1 and stack[-1][0] > indent:
            stack.pop()

        container = stack[-1][1]

        # If container is a list (shouldn't happen here), skip
        if isinstance(container, list):
            i += 1
            continue

        # Determine if value is empty (next block) or a scalar
        val_stripped = val.split('#')[0].strip() if '#' in val and '${' not in val else val
        val_stripped = val_stripped.strip()

        if not val_stripped:
            # Look ahead to determine mapping vs list
            next_content = ''
            for j in range(i + 1, len(lines)):
                nxt = lines[j].strip()
                if nxt and not nxt.startswith('#'):
                    next_content = nxt
                    break

            if next_content.startswith('- '):
                lst = []
                container[key] = lst
                stack.append((indent + 2, lst))
            else:
                mapping = {}
                container[key] = mapping
                stack.append((indent + 2, mapping))
        else:
            container[key] = parse_value(val_stripped)

        i += 1

    return root


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        # Return a minimal default (no providers)
        return {"providers": [], "noise": {}, "schedule": {}}
    return parse_yaml(CONFIG_FILE.read_text())


def load_topics(cfg: dict) -> list:
    tf = cfg.get("noise", {}).get("topics_file")
    if tf:
        p = BASE_DIR / tf
        if p.exists():
            return [l.strip() for l in p.read_text().splitlines() if l.strip()]
    if TOPICS_FILE.exists():
        return [l.strip() for l in TOPICS_FILE.read_text().splitlines() if l.strip()]
    return BUILTIN_TOPICS


# ── Logging ───────────────────────────────────────────────────────────────────

def log(msg: str, also_print: bool = True):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    if also_print:
        print(line)
    fd = os.open(LOG_FILE, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    with os.fdopen(fd, "a") as f:
        f.write(line + "\n")


# ── HTTP helpers ──────────────────────────────────────────────────────────────

def _post(url: str, headers: dict, payload: dict, timeout: int = 25) -> dict:
    _validate_provider_url(url)
    ctx = ssl.create_default_context()
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        return json.loads(resp.read())


def fire_anthropic(provider: dict, prompt: str, max_tokens: int) -> str:
    data = _post(
        url=provider["base_url"].rstrip("/") + "/messages",
        headers={
            "x-api-key": provider["api_key"],
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        payload={
            "model": provider["model"],
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        },
    )
    return data["content"][0]["text"]


def fire_openai(provider: dict, prompt: str, max_tokens: int) -> str:
    data = _post(
        url=provider["base_url"].rstrip("/") + "/chat/completions",
        headers={
            "Authorization": f"Bearer {provider['api_key']}",
            "Content-Type": "application/json",
        },
        payload={
            "model": provider["model"],
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        },
    )
    return data["choices"][0]["message"]["content"]


DISPATCH = {
    "anthropic": fire_anthropic,
    "openai":    fire_openai,
}


def fire_provider(provider: dict, prompt: str, max_tokens: int) -> bool:
    name  = provider.get("name", "unknown")
    style = provider.get("style", "openai")
    key   = provider.get("api_key", "")

    if not key:
        log(f"  ⚠️  {name}: no api_key — skipping")
        return False

    log(f'  → {name} | {provider["model"]} | tokens={max_tokens}')

    fn = DISPATCH.get(style)
    if fn is None:
        log(f"  ✗ {name}: unknown style '{style}'")
        return False

    try:
        fn(provider, prompt, max_tokens)
        log(f'  ✓ {name}: ok')
        return True
    except urllib.error.HTTPError as e:
        log(f"  ✗ {name}: HTTP {e.code}")
    except Exception as e:
        log(f"  ✗ {name}: error")
    return False


# ── Provider selection strategies ────────────────────────────────────────────

def select_providers(providers: list, strategy: str) -> list:
    if not providers:
        return []

    if strategy == "round-robin":
        import fcntl
        state_path = str(BASE_DIR / ".rr_state.json")
        with open(state_path, "a+") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.seek(0)
            try:
                idx = json.loads(f.read()).get("idx", 0)
            except (json.JSONDecodeError, ValueError):
                idx = 0
            selected = [providers[idx % len(providers)]]
            f.seek(0)
            f.truncate()
            f.write(json.dumps({"idx": (idx + 1) % len(providers)}))
        return selected

    if strategy == "weighted":
        weights = [max(p.get("weight", 1), 1) for p in providers]
        # pick 1-2 based on weights
        k = _randint(1, min(2, len(providers)))
        chosen = _weighted_choices(providers, weights, k)
        # deduplicate preserving order
        seen = set(); result = []
        for p in chosen:
            pid = id(p)
            if pid not in seen:
                seen.add(pid); result.append(p)
        return result

    # default: random
    k = _randint(1, min(2, len(providers)))
    return _sample(providers, k)


# ── Stats ─────────────────────────────────────────────────────────────────────

def show_stats():
    if not LOG_FILE.exists():
        print("No log file yet.")
        return

    lines = LOG_FILE.read_text().splitlines()
    runs = sum(1 for l in lines if "run started" in l)
    ok   = sum(1 for l in lines if "✓" in l)
    fail = sum(1 for l in lines if "✗" in l)
    print(f"Total runs  : {runs}")
    print(f"Successful  : {ok}")
    print(f"Failed      : {fail}")
    if lines:
        print(f"First entry : {lines[0][:30]}")
        print(f"Last entry  : {lines[-1][:30]}")


# ── Cron install ──────────────────────────────────────────────────────────────

def install_cron(cfg: dict):
    schedule = cfg.get("schedule", {})
    base = schedule.get("base_interval_minutes", 120)

    script = Path(__file__).resolve()
    cron_line = f"*/{base} * * * * python3 {shlex.quote(str(script))} 2>> {shlex.quote(str(LOG_FILE))}\n"

    import subprocess
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    existing = result.stdout if result.returncode == 0 else ""

    if str(script) in existing:
        print("ghostprint is already in crontab.")
        return

    new_cron = existing + cron_line
    proc = subprocess.run(["crontab", "-"], input=new_cron, text=True)
    if proc.returncode == 0:
        print(f"✅ Cron installed: every {base} min + jitter")
        print(f"   {cron_line.strip()}")
    else:
        print("❌ Failed to install cron. Add manually:")
        print(f"   {cron_line.strip()}")


# ── Main ──────────────────────────────────────────────────────────────────────

def run(cfg: dict, immediate: bool = False):
    log("👻 ghostprint — run started")

    schedule = cfg.get("schedule", {})
    noise_cfg = cfg.get("noise", {})

    # Apply jitter unless immediate
    if not immediate:
        jitter_min = schedule.get("jitter_minutes", 20)
        sleep_secs = _randint(0, jitter_min * 60)
        log(f"  ⏱  jitter: sleeping {sleep_secs // 60}m {sleep_secs % 60}s")
        time.sleep(sleep_secs)

    providers = cfg.get("providers", [])
    if not providers:
        log("  ⚠️  no providers configured — edit config.yaml")
        return

    strategy  = noise_cfg.get("strategy", "random")
    max_tokens = noise_cfg.get("max_tokens", 60)
    topics    = load_topics(cfg)

    selected = select_providers(providers, strategy)
    log(f"  strategy={strategy} | firing {len(selected)} provider(s)")

    for p in selected:
        prompt = _choice(topics)
        fire_provider(p, prompt, max_tokens)
        if len(selected) > 1:
            time.sleep(_uniform(1, 5))

    log("✅ done\n")


def main():
    parser = argparse.ArgumentParser(description="ghostprint — LLM noise injector")
    parser.add_argument("--run-once",      action="store_true", help="Fire immediately, no jitter")
    parser.add_argument("--install-cron",  action="store_true", help="Install to crontab")
    parser.add_argument("--stats",         action="store_true", help="Show stats from log")
    args = parser.parse_args()

    cfg = load_config()

    if args.stats:
        show_stats(); return
    if args.install_cron:
        install_cron(cfg); return

    run(cfg, immediate=args.run_once)


if __name__ == "__main__":
    main()
