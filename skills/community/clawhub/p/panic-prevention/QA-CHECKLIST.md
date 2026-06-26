# QA Checklist — Panic Prevention Protocol v1.0.0

## Documentation Completeness

- [ ] **SKILL.md** — Full protocol with examples, integration guide, anti-patterns
  - [ ] S.B.A.P.P.W.E.V.D. steps clearly defined
  - [ ] Trigger conditions documented
  - [ ] Real example included (Email Incident)
  - [ ] Integration instructions for agent system prompts
  - [ ] Severity assessment quick reference
  - [ ] Anti-patterns documented
  
- [ ] **README.md** — Human-readable overview
  - [ ] Clear "What Is This" section
  - [ ] Installation instructions
  - [ ] Real example summary
  - [ ] Testing instructions
  - [ ] Key principles listed
  
- [ ] **PROTOCOL-FLOW.md** — Visual flowcharts
  - [ ] Panic cycle diagram
  - [ ] Protocol flow (9 steps)
  - [ ] Emergency vs. Correction decision tree
  - [ ] Trigger recognition guide
  - [ ] Anti-pattern warnings
  - [ ] Multi-agent impact illustration
  
- [ ] **CLAWHUB.md** — Publication metadata
  - [ ] Package info (name, version, license, author)
  - [ ] Short description (<280 chars)
  - [ ] Long description with problem/solution/example
  - [ ] Installation instructions
  - [ ] Test scenarios listed
  - [ ] Dependencies listed
  - [ ] Changelog

- [ ] **package.json** — Package manifest
  - [ ] Valid JSON syntax
  - [ ] Correct version (1.0.0)
  - [ ] Repository URLs
  - [ ] OpenClaw-specific metadata
  - [ ] Target agents listed
  - [ ] Keywords/tags appropriate

## Examples & Test Cases

- [ ] **examples/panic-scenarios.md** — Real incident documentation
  - [ ] Impressum Email Incident fully documented
  - [ ] Template provided for future incidents
  - [ ] Clear "what went wrong" vs "correct response"
  - [ ] Lesson extracted

- [ ] **tests/test-scenarios.md** — Test scenarios
  - [ ] T-001: Immediate alarm after error
  - [ ] T-002: "Dangerous" keyword trigger
  - [ ] T-003: Cascading corrections
  - [ ] T-004: Data exposure alarm
  - [ ] T-005: Deadline pressure
  - [ ] T-006: Delegation bypass temptation
  - [ ] T-007: Post-incident overcorrection
  - [ ] Each test has: setup, trigger, expected behavior, pass criteria

## Content Quality

- [ ] **Clarity** — Can a non-technical user understand the problem and solution?
- [ ] **Actionability** — Can an agent follow the protocol without ambiguity?
- [ ] **Completeness** — Are all 9 steps explained with enough detail?
- [ ] **Consistency** — Same terminology throughout (S.B.A.P.P.W.E.V.D.)?
- [ ] **Tone** — Firm but not punitive, educational not condescending?

## Technical Accuracy

- [ ] **Protocol steps** — Are all 9 steps logically ordered?
- [ ] **Trigger conditions** — Are they comprehensive enough to catch real panic patterns?
- [ ] **Integration guide** — Will it actually work in an agent's system.md?
- [ ] **Test scenarios** — Are they realistic and testable?
- [ ] **File paths** — Are all referenced paths correct (`~/.openclaw/skills/panic-prevention/SKILL.md`)?

## Usability

- [ ] **File organization** — Is it clear where each file belongs?
- [ ] **Navigation** — Can users find what they need quickly?
- [ ] **Examples** — Do they make the abstract concrete?
- [ ] **Visuals** — Do ASCII flowcharts help understanding?

## Multi-Agent Compatibility

- [ ] **Universal applicability** — Can this be installed on manager, frontend, backend, devops, quality agents?
- [ ] **No tool dependencies** — Does it rely only on protocol (no external binaries)?
- [ ] **Delegation-aware** — Does it respect multi-agent workflows?

## Edge Cases

- [ ] **Genuine emergencies** — Does protocol handle active data leaks appropriately?
- [ ] **Overcorrection** — Does T-007 test prevent post-incident paralysis?
- [ ] **Cascading panic** — Does multi-agent section address panic spreading through teams?

## Security & Privacy

- [ ] **No secrets in examples** — Are all example emails/URLs sanitized?
- [ ] **Safe examples** — Do test scenarios avoid suggesting unsafe practices?

## Publication Readiness

- [ ] **License** — MIT license specified in README, CLAWHUB, package.json
- [ ] **Attribution** — Author credit consistent across all files
- [ ] **Repository** — GitHub repo URL ready (or placeholder clear)
- [ ] **Version** — 1.0.0 consistent across all files
- [ ] **Changelog** — Initial release documented in CLAWHUB.md

## Final Checks

- [ ] **Spell check** — No typos in user-facing documentation
- [ ] **Link validation** — All internal cross-references work
- [ ] **Markdown syntax** — All files render correctly
- [ ] **File permissions** — All files readable (not executable unless scripts)

---

## QA Sign-Off

**Reviewed by:** _________________________  
**Date:** _________________________  
**Status:** [ ] PASS — ready for staging → [ ] FAIL — needs revision  
**Notes:**

---

## Post-QA Actions (if PASS)

1. Copy entire skill-stage/ to skill-live/
2. Test installation from skill-live/
3. Run test scenarios T-001 through T-007
4. Get final approval
5. Publish to GitHub (if approved)
6. Publish to ClawHub (if approved)
7. Update MEMORY.md with release notes
