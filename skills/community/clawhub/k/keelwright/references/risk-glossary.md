# Risk Glossary — 28 failure modes keelwright covers

> **Source:** Consolidated from `security-gates.md` (R1-R12), vibe/loop-coding literature (Stanford, Veracode, QA-trap-catalog), and operational incidents.
> **Purpose:** Give every agent/operator a shared vocabulary. Each risk maps to a machine-enforced gate (where possible) and a human-check fallback.
> **Usage:** Load on demand via `skill_view(name='keelwright', file_path='references/risk-glossary.md')`.

---

## The 28 Risks (R1-R28)

| # | Risk ID | Short Name | Description | Gate / Mitigation | Blocks? |
|---|---------|------------|-------------|-------------------|---------|
| 1 | **R1** | Insecure code (OWASP) | SQLi, XSS, path traversal, SSRF, deserialization, crypto misuse | Gate 1: Gitleaks + Semgrep (authoritative) | YES |
| 2 | **R2** | Secret leak | API keys, tokens, passwords in code, logs, config, .env | Gate 1: Gitleaks on staged + history | YES |
| 3 | **R3** | Business-logic hole | Auth bypass on edge case, permission logic flaw, IDOR | Gate 2: Independent reviewer subagent (fresh context) | YES |
| 4 | **R4** | 80% problem (tech debt) | Agent delivers 80% of feature, silently skips critical 20% (tests, errors, edge cases) | Gate 3: Production-readiness checklist | YES (critical paths) |
| 5 | **R5** | Design for failure | No timeouts, no retry, no fallback, no circuit breaker, no dead-letter handling | Gate 4: Fault checklist (timeout/retry/fallback/breaker) | WARNING |
| 6 | **R6** | False security | "Looks ok" → skip machine check; log shows masked secret but value leaked | Gate 1/6: Never trust eyeball; always run tools; constant logging only | META |
| 7 | **R7** | Reasoning-action disconnect | Agent says "I added tests" but diff shows none; says "fixed" but bug persists | Gate 2/7: Compare "said" vs "in the diff" (subagent reviewer) | WARNING |
| 8 | **R8** | Slopsquatting (hallucinated pkg) | ~20% of LLM-suggested packages don't exist or are typosquatted | Gate 5: Verify existence/age + GuardDog BEFORE install | YES |
| 9 | **R9** | Model version drift | Model silently upgraded/downgraded; behavior changes without notice | Gate 8: Pin model+version in run contract; re-validate on change | WARNING |
| 10 | **R10** | Multi-agent cascade + memory poisoning | Agent A writes bad memory → Agent B reads it → cascading failure | Gate 9: Isolate outputs; durable memory only after verify | WARNING |
| 11 | **R11** | Malicious third-party skill | Skill with hidden payload (zip-slip, post-install, supply-chain) | Gate 10: SkillSpector audit BEFORE install; ZIP-slip guard | YES |
| 12 | **R12** | Scope creep / CONFLICT-resolution | Unbounded loops, auto-merge conflicts, lost safety process during rebase | Gate 11: Explicit CONFLICT-resolution process (T53) | YES |
| 13 | **R13** | Loop design / unbounded iteration | No max-iterations, no progress metric, infinite repair cycle | Gate 11: Termination conditions (max-3, escalation) | YES |
| 14 | **R14** | Compaction / context loss | Agent forgets earlier findings; repeats work; loses "done" criteria | Gate 11: PROGRESS.md + session_search + memory tool | WARNING |
| 15 | **R15** | Rate limiting / budget exhaustion | API quota hit, token budget blown, tool-call caps exceeded | Gate 11: Tool call budgets (10 shell / 5 files / 3 MCP) | WARNING |
| 16 | **R16** | Phoenix / rollback failure | Cannot revert to known-good; no git tag; no rollback path | Gate 11: Git tags per version; `git revert` protocol | YES |
| 17 | **R17** | Match loop / false equivalence | "Same output" ≠ same behavior; benchmark arm invalidated | Gate 2: Never hand-resolve benchmark arm; re-run on main | YES |
| 18 | **R18** | Model drift (behavioral) | Same model+version, different output distribution over time | Gate 8: Pin + periodic re-validation; drift detection | WARNING |
| 19 | **R19** | Malicious skill (supply chain) | Compromised dependency, transitive attack, maintainer account takeover | Gate 10: SkillSpector + GuardDog + pinned SHA; verify provenance | YES |
| 20 | **R20** | Memory poisoning | Adversarial input written to durable memory; affects future sessions | Gate 9: Write memory ONLY after verify; isolate per-session | WARNING |
| 21 | **R21** | Regression / silent skip | Previously fixed bug reintroduced; test passes but logic changed | Gate 3: Regression test required for every fix; breaker.py | YES |
| 22 | **R22** | Human bottleneck | Operator must approve every step; flow stalls; "LGTM" without reading | Gate 2/11: Parallel subagents; async verification; auto-merge safe | WARNING |
| 23 | **R23** | Confabulation / hallucination | Agent invents functions, files, URLs, versions, CLI flags | Gate 1/6: Verify in session (web_search, --help, read_file) | WARNING |
| 24 | **R24** | Tool call / shell injection | User input reaches `shell=True` or unsanitized argv | Gate 1: No shell=True; argv lists only; input validation | YES |
| 25 | **R25** | Path traversal / zip-slip | `../../etc/passwd` in extracted archive; symlink escape | Gate 10: `extract_skill()` resolves + rejects escapes | YES |
| 26 | **R26** | Data exfiltration / PII leak | Logs, memory, telemetry contain secrets, user data, operator identity | Gate 1/9: No private paths; expanduser("~") only; constant logs | YES |
| 27 | **R27** | License / attribution violation | MIT-0 header missing; copied code without SPDX; license changed | Gate 4: 21/21 .py have MIT-0; audit on every add | YES |
| 28 | **R28** | Config drift / env mismatch | Local works, CI fails; docker vs bare metal; Windows vs Linux paths | Gate 3/11: Windows MSYS paths → native; cygpath; PYTHONPATH= | WARNING |

---

## Quick Reference by Category

### Code Security (R1, R2, R3, R24, R25)
- **R1** Insecure code (OWASP) — Semgrep auto
- **R2** Secret leak — Gitleaks auto
- **R3** Business logic — Independent reviewer
- **R24** Shell injection — No shell=True (enforced)
- **R25** Path traversal — ZIP-slip guard

### Loop/Process Safety (R4, R5, R13, R14, R15, R16, R17)
- **R4** 80% problem — Prod checklist
- **R5** Design for failure — Fault checklist
- **R13** Unbounded loop — Max-3 + escalation
- **R14** Compaction loss — PROGRESS.md + memory
- **R15** Budget exhaustion — Tool call budgets
- **R16** Rollback failure — Git tags per release
- **R17** Match loop — Re-run on main, no hand-resolve

### Model/Supply Chain (R8, R9, R11, R18, R19, R23)
- **R8** Slopsquatting — GuardDog + verify
- **R9** Model drift — Pin + re-validate
- **R11** Malicious skill — SkillSpector audit
- **R18** Behavioral drift — Periodic re-validation
- **R19** Supply chain — Pinned SHA + provenance
- **R23** Confabulation — Verify in session

### Memory/State (R10, R20, R26)
- **R10** Cascade + poisoning — Isolate + verify-before-write
- **R20** Memory poisoning — Verify before durable write
- **R26** PII/exfiltration — No private paths, constant logs

### Governance (R6, R7, R12, R21, R22, R27, R28)
- **R6** False security — Machine check mandatory
- **R7** Reasoning-action gap — Diff vs said
- **R12** Conflict resolution — T53 process
- **R21** Regression — Breaker + regression tests
- **R22** Human bottleneck — Parallel + async
- **R27** License — MIT-0 enforced
- **R28** Config drift — Native paths, PYTHONPATH=

---

## How to Use

1. **In a loop session:** When you hit a pattern that feels risky, check the table. "Is this R4 (80% problem)? If yes → run Gate 3 checklist."
2. **In a review:** Reviewer subagent reads this + `security-gates.md` + `requesting-code-review` skill.
3. **In a retro:** Map each incident to a Risk ID. If a risk has no gate → propose new gate.
4. **For new agents:** This glossary is the shared vocabulary. Load it once at session start.

---

## Cross-References

- **R1-R12 implementations** → `references/security-gates.md` (machine-enforced gates)
- **R13-R28 gates** → this file
- **T53 CONFLICT-resolution (R12)** → `references/conflict-resolution.md`
- **Loop termination** → `references/circuit-breaker.md`
- **Build phases** → `references/phases.md`
- **Coding discipline** → `references/writing-code.md`
- **Runtime-agnostic web guard** → `references/web-guard.md`
- **External skill audit tools** → `references/external-skill-audit-tools.md`
- **Provenance / adapted sources** → `references/provenance.md`

---

*Generated as part of keelwright v1.10.1 P0 fixes. Kept in sync with `security-gates.md` and operational incidents.*