## 6a. Share Procedure — Submit to Nous Research Optional Skills

Use when the user says "share this skill", "submit to Nous", "publish to optional-skills", or "contribute this skill". Prerequisites: score ≥45/50, `description` ≤ 60 chars, no PII/credentials, **`scripts/secret-scan.sh` exits 0 (CLEAN)**, test file exists. Steps: prepare submission dir → copy files → clean frontmatter → verify no PII → run tests → py_compile scripts → commit to fork → create PR.  for the full procedure.

**Mandatory Configuration Policy gate (the single most common auto-close reason):** Behavioral settings (thresholds, retention windows, feature flags, display prefs, paths) MUST NOT be read from environment variables — the hermes-sweeper auto-closes such PRs under the `env-var-for-config` policy and the closed PR **cannot be reopened via API** (a maintainer must reopen, or you open a fresh PR). Correct mechanism: declare each setting in `metadata.hermes.config`, read it at runtime from `$HERMES_HOME/config.yaml` under `skills.config.<key>` (via PyYAML — `telephony.py` is the reference impl), document `skills.config.<key>` in SKILL.md (never env-var names), and let CLI flags override. Only secrets go in `.env`; only `HERMES_HOME`/`HERMES_PROFILE` locate the runtime.

Run the automated check before opening the PR:
```bash
python3 <forge>/scripts/forge_audit_skills.py --skill <ocas-name>   # 0 exit = clean
```
It flags any `GENIE_*` / non-secret env-var config read in `scripts/` or env-var config table in `SKILL.md`. Also confirm there are no drifted copies: genie, for example, had the running script, a skill-bundled script, and THREE divergent SKILL.md files — fix ALL copies, not just the one you diff. The full written standard: `references/nous-skill-requirements.md` (Configuration Policy) + `ocas-forge`'s `references/compliance-audit-checklist.md`.

---
- `research/` — Academic search, data analysis, OSINT
- `communication/` — Email, messaging, social media
- `security/` — Penetration testing, forensics, auditing
- `mlops/` — ML training, fine-tuning, inference
- `blockchain/` — Crypto, DeFi, NFTs
- `finance/` — Trading, modeling, analysis
- `gaming/` — Game servers, emulators
- `health/` — Fitness, nutrition, medical
- `payments/` — Payment processing, billing
- `web-development/` — Frontend, backend, full-stack
- `software-development/` — Code review, debugging, testing
- `mcp/` — MCP server integrations
- `dogfood/` — Agent self-improvement, testing
- `migration/` — Data migration, onboarding
- `autonomous-ai-agents/` — Subagent orchestration

### Gotchas

- **Description length is enforced:** The CONTRIBUTING.md has `assert len(description) <= 60`. A skill with a 100+ char description will be rejected. Be aggressive — cut articles, merge phrases, use short words.
- **No external dependencies:** Skills should use stdlib + existing Hermes tools. If a skill requires pip packages, it belongs in Skills Hub, not optional-skills.
- **Tests are required:** Every skill needs `tests/test_<skill>_skill.py` with at least import, help, dry-run, and frontmatter tests.
- **Author is the agent:** Use the agent's own name/GitHub, not the user's. The user directs, the agent authors.
- **No user data:** Never include the user's name, email, paths, or personal config in the submitted skill. All paths should be generic (`~/.hermes/`, `<fs-root>/`, etc.).

See `references/skill-sanitize-checklist.md` for the full sanitize procedure.

---