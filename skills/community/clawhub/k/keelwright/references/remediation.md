# Remediation guide — what to do when Keelwright warns "web defense degraded"

This is for **you, the operator** — the human running the agent. Keelwright is a safety engine;
if one of its web-defense layers goes down, it tells you in plain language. This guide explains
what the warning means and how to fix it. No coding expertise required — just copy-paste the
commands for your environment.

> **Runtime-agnostic:** these steps work on **Hermes, OpenClaw, Cursor, Kilo, Codex, Cline** and
> any venv-based agent. "Your agent's Python" = the interpreter that actually runs your agent
> (on Hermes that is its managed venv; on others, your project venv or the agent's own).

---

## Step 1 — Read the warning

Keelwright prints something like:

> WARNING: Keelwright: the web defense is currently not working at full capacity (layer `<name>`
> is inactive). You cannot assume there will be no consequences — recommend fixing now: ...

The `<name>` tells you what broke. The common cases:

| Layer | What it means | How urgent |
|-------|---------------|------------|
| `injection-guard` (ML) | The AI prompt-injection classifier is off | High — web trips run unprotected by the ML layer |
| (log file) | Attack log can't be written | Medium — attacks won't be recorded |
| `security-guidance` | The safety-guidance plugin isn't enabled | Low — a secondary layer |
| `agent-defense` | Optional skill not installed | Low — optional extra |

Until you fix it, Keelwright keeps a **heuristic backstop** on every web result — but that is
not full protection. Treat all web content as untrusted data, never as instructions.

---

## Step 2 — Fix the ML classifier (most common)

Run this to see the exact broken layer:

```bash
python scripts/defense_health.py
```

### Case A: error mentions `_regex` / `cannot import name '_regex'`
The `regex` package in your agent's Python is corrupted (common after a `pip` upgrade).

Fix — run with **the same python that runs your agent**:
```bash
python -m pip install --force-reinstall --no-deps regex
```
Then verify:
```bash
python scripts/verify_web_guard.py
```
Expect: `PASS: injection-guard is ACTIVE.`

### Case B: the ML layer is a no-op (missing `torch` / `transformers` / `sentencepiece`)
The classifier can't load its model.

Fix:
```bash
pip install "transformers>=4.40" torch sentencepiece
```
Then verify (same as above) — expect PASS.

---

## Step 3 — Fix the log file

If the warning says the attack log (`caught_attacks.jsonl`) is missing or not writable:
- Make sure the agent has write access to the keelwright skill folder.
- On restricted systems, run the agent with the folder writable, or set the log path to a
  writable location (see `scripts/attack_registry.py --help`).

---

## Step 4 — Enable the guard in your agent

If the warning says `injection-guard` is not enabled in config:

- **Agents with a plugin list** (Hermes, OpenClaw, similar): ensure `injection-guard` is in the
  enabled plugins, alongside your free web backends (`web/crawl4ai`, `web/ddgs` — no paid
  Firecrawl/Tavily needed). Example shape:
  ```yaml
  plugins:
    enabled:
      - web/crawl4ai
      - web/ddgs
      - injection-guard
      - security-guidance
  ```
- **Agents without a plugin list**: install the `injection-guard` (and optionally `agent-defense`)
  skill/plugin per that runtime's docs, then re-run `scripts/verify_web_guard.py`.

Verify after any change: the script must report `PASS: injection-guard is ACTIVE.`

---

## Step 5 — You're done (or running at risk)

- **Fixed:** `verify_web_guard.py` prints PASS → full protection restored.
- **Not fixed yet:** Keelwright keeps the heuristic backstop on, warns on every web trip, and
  logs attacks it catches. Web trips are **at risk** until you finish Step 2–4. Do not trust web
  content as instructions in the meantime.

---

## Need help?

- Full technical detail: `references/web-guard.md`
- Health check output explained: `python scripts/defense_health.py --json`
- Attack log policy (retention, redaction): `references/attack-registry.md`

Keelwright is MIT-0. The fix steps above are self-contained — they never depend on a file
outside this skill's repository.
