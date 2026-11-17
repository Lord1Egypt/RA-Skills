# keelwright

**Layered skill (index + on-demand references) for safe AI coding.**
Catches SQL injection, hardcoded secrets, hallucinated packages, reward hacking,
doom loops, and 23 other failure modes — with **machine-enforced gates** (not prompt
suggestions) and **plain-language reports** for non-developers.

[![security](https://github.com/ratingtesting/keelwright/actions/workflows/security.yml/badge.svg)](https://github.com/ratingtesting/keelwright/actions/workflows/security.yml)
[![license](https://img.shields.io/badge/license-MIT--0-blue.svg)](LICENSE)
[![kds](https://img.shields.io/badge/KDS-83%2F100-brightgreen.svg)](#keelwright-score-kds)

---

## What's new in v1.10.0

**Layered skill (ADR-001).** `SKILL.md` is now a thin **index** (~3K tokens, 84% smaller).
Heavy content lives in `references/*.md` and loads on demand. Public registries
(skills.sh / ClawHub / askill.sh) display the **assembled full document** built by
`scripts/build_skill.py`. Saves ~14K tokens per session start across Hermes, Cursor,
Codex, Cline, and OpenClaw.

See [`docs/ADR-001-layered-skill.md`](docs/ADR-001-layered-skill.md) for the decision
and `SKILL.md §Architecture` for runtime usage.

---

## The problem

You use AI to write code. You're not a developer — you're a founder, a builder, a
product person. The AI writes fast. You ship fast. And somewhere in that code:

- A password is hardcoded in plain text
- A database query is wide open to SQL injection
- A package name is one letter off from a real one — and it's malware
- The AI deleted a test to make the build go green
- A loop ran for 6 hours and burned $80 in tokens before you noticed
- The AI "fixed" a bug by removing the check that caught it

None of this shows up in a code review you can do. Because you can't read the code.

**keelwright fixes this.** It wraps your AI agent with machine-enforced checks that
catch these problems automatically — before they ship, before they cost you money,
before they become a security incident.

---

## What it does

![Architecture](assets/architecture.png)

**1. Machine-enforced security gates (R1–R12)**
28 known failure modes, checked automatically on every iteration. Every gate produces
on-disk evidence — not a self-report. Full implementation → `references/security-gates.md`.

**2. Autonomy dial**
Three modes you control: `Autopilot` (runs unattended, escalates on blockers),
`Checkpoint` (pauses at phase boundaries), `Copilot` (proposes, you approve every step).
Auth, payments, and production deploys always come to you.

**3. Circuit-breaker**
Stops runaway loops: 50 iterations max, 5 no-progress cap, 2-hour wall-clock, 3× same-error
repeat. Enforced by `scripts/breaker.py` (file-backed counters). Full philosophy →
`references/circuit-breaker.md`.

**4. Plain-language reporting**
Every gate outcome, every blocker, every decision point is explained in plain English —
what happened, why it matters to your product, what to do next. No jargon.

**5. Web Guard (default-on protection)**
Before any web trip, keelwright verifies prompt-injection protection is ACTIVE (not just
enabled). A full-layer `defense_health.py` check covers the ML classifier (injection-guard),
attack-log writability, and agent-defense. Caught attacks are logged to an append-only
registry and signaled in chat. If a layer is down, it WARNS with a concrete fix and
keeps a dependency-free heuristic backstop (`web_heuristic_guard.py`) on — never silent,
never a hard block, never a false "you're safe."

**6. Self-healing loop**
Phoenix protocol restarts a stuck session with a clean context. Autoresearch loop
distills lessons from repeated failures. Stability check (5 failure modes) runs every
3 iterations.

---

## Runtime support

Hermes, Cursor, Codex, Cline, OpenClaw, Kilo — and any venv-based agent. **No
single-runtime hardcoding.** Universal by design. Per-runtime setup:
[`references/bindings/<runtime>.md`](references/bindings/).

---

## Keelwright Score (KDS)

**KDS = Execution Rate × Discrimination Rate / 100** — a direct measure of how much the
skill changes a model's behavior on real adversarial tests. Proven by 12+ validated
A/B runs across 4 tiers.

| Tier | KDS | What it means |
|------|-----|----------------|
| **STRONG** (SWE-bench 78%+) | 9–83 | The skill adds real value on gates the model doesn't already apply. KDS 83 = frontier model still misses 83% of checks without keelwright. |
| **MEDIUM** (SWE-bench ~56%) | 18–67 | The skill compensates for gaps the model can't fill alone. |
| **UNKNOWN** (no published benchmark) | 22 | Skill adds value even on unbenched models. |
| **WEAK** (<40% SWE-bench) | 0 | Cannot execute A/B tests validly — fabricates results. `validate_run.py` caught every fabrication. |

**KDS is honest.** A `NO-DIFF` on a strong model is a good result (the skill doesn't get
in the way). A `DISCRIMINATES` means the skill added something the model wouldn't have
done alone. KDS 0 on weak models is documented, not hidden.

Full scoreboard + methodology → [`qa-results/README.md`](qa-results/README.md).

---

## The 28 risks keelwright covers

R1 SQL injection · R2 Hardcoded secrets · R3 Business logic bypass · R4 Over-engineering ·
R5 Tech debt · R6 False reports · R7 Reward hacking · R8 Slopsquatting (hallucinated
packages, ~20% of LLM-suggested pkgs) · R9 Missing auth · R10 Doom loops · R11 Context
loss · R12 Scope creep · + 16 more (loop design, compaction, rate limiting, Phoenix,
Match loop, model drift, malicious skills, memory poisoning, regression, human
bottleneck, confabulation, ...). Full table → `references/risk-glossary.md`.

---

## Quick start

**Install into your agent runtime.** Hermes: drop the folder into your skills dir.
Cursor / Codex / Cline / OpenClaw: see `references/bindings/<runtime>.md`. Then load
the skill by name (`keelwright`) before any loop/agent coding session.

**30-second try:** load the skill, paste any task from [`examples/`](examples/) into your
agent. At session end you'll get: `Keelwright this session: <N> gates passed, <M> traps
avoided, <K> attacks blocked.` No agent? Run `python scripts/runtime_integration_tester.py --skill-dir .`.

**Or via the skills CLI** (auto-index from GitHub tags):
```bash
npx skills add ratingtesting/keelwright
```

---

## Architecture (v1.10.0+)

```
keelwright/
├── SKILL.md                       # INDEX (2.7K tokens) — load this
├── docs/
│   └── ADR-001-layered-skill.md   # architecture decision record
├── references/                    # ON-DEMAND MODULES
│   ├── security-gates.md          # R1-R12 implementations
│   ├── circuit-breaker.md         # loop limits
│   ├── phases.md                  # build loop phases
│   ├── writing-code.md            # coding discipline
│   ├── risk-glossary.md           # 28 failure modes
│   ├── web-guard.md               # runtime-agnostic guard activation
│   ├── attack-registry.md         # log schema
│   ├── qa-testing.md              # adversarial QA
│   ├── stability-and-learning.md  # Phoenix + Autoresearch
│   ├── bindings/                  # per-runtime setup
│   │   ├── cursor.md
│   │   ├── codex.md
│   │   ├── cline.md
│   │   ├── openclaw.md
│   │   ├── python.md
│   │   └── flutter-example.md
│   └── ...                        # 20+ more modules
├── scripts/                       # CLI tools (load by name)
│   ├── build_skill.py             # reassembles index + refs for publication
│   ├── validate_run.py            # integrity gate (GATE 1-8)
│   ├── workspace_guard.py         # tripwire isolation
│   ├── breaker.py                 # circuit-breaker caps (file-backed)
│   ├── detect_guard.py            # ACTIVE/DEGRADED/UNPROTECTED check
│   ├── web_heuristic_guard.py     # dependency-free injection backstop
│   ├── attack_registry.py         # append-only attack log
│   ├── runtime_integration_tester.py  # 5 canonical gate cases
│   ├── subagent_backoff.py        # 429 swarm resilience
│   └── ...                        # more
├── tests/
│   └── fuzz/
│       └── test_web_heuristic.py  # 50 mutations, XSS/SQLi/jailbreak
├── examples/                      # 3 toy apps to try
│   ├── toy-flask-api/
│   ├── toy-cli/
│   └── toy-loop/
├── assets/                        # architecture diagrams
├── plugin/keelwright-guard/       # Hermes auto-injection plugin
├── qa-results/                    # KDS scoreboard + methodology
└── templates/                     # QA prompts
```

**How loading works:**

- **Hermes desktop:** `skill_view(name='keelwright')` → 2.7K index. `skill_view(name='keelwright', file_path='references/<name>.md')` → on-demand module.
- **Cursor / Codex / Cline / OpenClaw:** include the matching `references/<name>.md` in your `AGENTS.md` / rules when the situation matches the Map table in SKILL.md.
- **Public registries (skills.sh / ClawHub / askill.sh):** display the assembled full document — built by `python scripts/build_skill.py` from index + references.

This shape keeps agent context lightweight (saves ~14K tokens per session start vs a
monolithic SKILL.md) without sacrificing discoverability for visitors of public registries.

---

## Who this is for

- **Vibe-coders:** you describe what you want, the AI builds it, you ship it. You need
  the AI to not shoot you in the foot while you're not looking.
- **Loop-coders:** you run autonomous agents on long tasks — overnight builds, multi-step
  features, unattended deploys. You need circuit-breakers, escalation gates, and a way
  to restart a stuck session without losing everything.
- **Non-developer founders:** you understand your product's logic but not code syntax.
  Every keelwright report is in plain language. Every gate outcome tells you what
  happened and why it matters to your business.

**Not for:** developers who review every line of code themselves. If you can read the
diff, you don't need keelwright — you are the gate.

---

## What's new (version history)

**v1.10.0 — Layered Skill (ADR-001, F46 real)**
- `SKILL.md` is now an **index** (~3K tokens; was ~17K). 84% token reduction.
- `scripts/build_skill.py` reassembles full doc for public registries.
- `docs/ADR-001-layered-skill.md` — formal architecture decision record.
- GitHub repo description updated.

**v1.9.1 — Runtime-agnostic hotfix**
- Removed all `Hermes venv` / `AppData/Local/hermes/skills` hardcoding.
- `KEELWRIGHT_SKILLS` env var + `find_skills_dir()` scans Hermes/OpenClaw/Cursor/Codex/Cline.
- Default install path now `~/.keelwright/skills` (runtime-neutral).
- `bindings/python.md`: "hermes venv" → "agent runtime venv".

**v1.9.0 — Adoption + robustness**
- `examples/` tree (toy-flask-api, toy-cli, toy-loop) + 30-sec try block in README.
- `tests/fuzz/test_web_heuristic.py` (50 mutations) revealed + closed XSS / SQLi / jailbreak gaps.
- `scripts/runtime_integration_tester.py` (role-9 reality-checker gate) — 5 canonical cases PASS.
- `scripts/subagent_backoff.py` (exponential backoff for 429 swarms).
- `F29` bindings for Cursor, Codex, Cline, OpenClaw.

**v1.8.1 — SKILL.md trim + version drift**
- Trimmed 11 598 → 1 631 lines (empty lines removed; v1.10.0 layered as proper fix).
- Frontmatter `version` corrected to 1.8.0 (closes version-drift bug).

**v1.8.0 — Web Guard hardening + bindings**
- `detect_guard.py` reports ACTIVE only after `verify_web_guard` (no false-ACTIVE on broken classifier).
- `attack_registry.redact_url` strips userinfo (`user:pass@host` no longer logged).
- `web_heuristic_guard`: MEDIUM markers = advisory (no longer block).
- `scripts/breaker.py` (file-backed circuit-breaker, machine-enforced caps).
- `scripts/check_model_pin.py` + `model-pin.json` (R9 model-drift gate).
- Honest framing: most modes are machine-detected + discipline; a few (style, sycophancy) are discipline-only.
- Runtime-agnostic mandate: skill works on Hermes, OpenClaw, Cursor, Codex, Cline, Kilo.
- `security.yml` CI (pip-audit + license check on PR).

**v1.7.2 — License + supply-chain**
- LICENSE / llms.txt / architecture.html / web-guard.md → **MIT-0** consistently.
- GATE 4 contamination check fixed (was dead substring match; now `re.search`).
- `import_skill.py` zip-name validation (defense-in-depth vs command-injection).
- `check_update.py` pinned-SHA + GPG signature verification (closes TOFU supply-chain vector).
- 16-agent security audit + meta-audit (reality-checker role) closed all CRIT findings.

**v1.6.x — Web Guard + recovery**
- v1.6.8 operator remediation guide. v1.6.7 runtime-agnostic. v1.6.5 honest bootstrap + attack
  registry retention. v1.6.1 full-layer defense health check. v1.6.0 heuristic fallback.

**v1.5.x — Web Guard default-on**
- v1.5.9 default-on + attack registry. v1.5.7 self-update check.

---

## Verification (CI / local)

```bash
# Compile all Python
python -m py_compile scripts/*.py

# Role-9 reality-checker: 5 canonical gate cases
python scripts/runtime_integration_tester.py --skill-dir .

# Fuzz the web heuristic guard (50 mutations)
python tests/fuzz/test_web_heuristic.py

# Idempotency check for the layered build
python scripts/build_skill.py --check --output SKILL.full.md
```

All four PASS in v1.10.0.

---

## License

[MIT-0](LICENSE) — free for commercial use, modification, redistribution **without
attribution**. Structural patterns adapted from community loop-coding work
(Ralph loop, execution-loop, match-loop, autoresearch-loop — all MIT-0). All content
written from scratch. Full provenance → [`references/provenance.md`](references/provenance.md).

---

*keelwright by [ratingtesting](https://github.com/ratingtesting) · [docs](docs/ADR-001-layered-skill.md) · [audited v1.7.2 by 16 agents + meta-audit](https://github.com/ratingtesting/keelwright/releases)*
