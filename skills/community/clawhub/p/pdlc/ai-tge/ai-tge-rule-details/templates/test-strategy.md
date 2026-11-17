<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Test Strategy — Template

---
generatedBy: AI-TGE
generatedVersion: {version}
source: architecture-package + development-workspace
generatedOn: {ISO-date}
ownership: generated
---

**Type:** Strategy
**Generated:** {ISO-date}
**Engine:** AI-TGE v{version}
**Mode:** {Full Chain / Architecture Only / Brownfield / Observation Only}
**Depth:** {Minimal / Standard / Comprehensive}
**Project:** {project_name}

---

## 1. Overview

{Brief summary: what this strategy governs, derived from {N} architectural commitments across {n} components. Key architectural characteristics that shape the testing approach.}

---

## 2. Test Pyramid

| Level | Target % | Current % | Rationale |
|-------|:--------:|:---------:|-----------|
| Unit | {n}% | {n}% | {why — based on register distribution and architecture} |
| Integration | {n}% | {n}% | {why} |
| System | {n}% | {n}% | {why} |
| Acceptance | {n}% | {n}% | {why} |

---

## 3. Testing Tools & Frameworks

| Purpose | Tool | Source |
|---------|------|--------|
| Unit testing | {framework} | DW tech-stack.md |
| Integration testing | {framework} | DW tech-stack.md |
| API contract testing | {framework} | DW tech-stack.md |
| E2E / acceptance testing | {framework} | DW tech-stack.md |
| Performance testing | {framework} | DW tech-stack.md or recommended |
| Coverage measurement | {tool} | DW tech-stack.md |
| Mocking / stubbing | {library} | DW tech-stack.md |

---

## 4. Coverage Goals

| Level | Target | Measurement Method | Timeline |
|-------|:------:|-------------------|----------|
| Unit | {n}% branch coverage | {coverage tool} | {by when} |
| Integration | {n}% of register entries covered | Register status tracking | {by when} |
| System | {n}% of register entries covered | Register status tracking | {by when} |
| Acceptance | {n}% of acceptance criteria covered | Register status tracking | {by when} |

**Baseline (brownfield):** {current coverage if known, or "N/A — greenfield"}
**Ramp strategy:** {incremental targets per sprint if brownfield}

---

## 5. Test Data Strategy

### Approach

{How test data is created, managed, and cleaned up for this project}

### By Test Level

| Level | Data Source | Isolation | Cleanup |
|-------|-----------|:---------:|---------|
| Unit | In-memory fixtures / factories | Complete — no external state | Auto (garbage collected) |
| Integration | {approach: test DB / containers / seeded} | Per test suite | Reset between suites |
| System | {approach: staging with synthetic data} | Shared environment | Managed state |
| Acceptance | Scenario-specific setup | Per scenario | After scenario |

### Data Considerations

- **Sensitive data:** {approach — synthetic only / anonymized / masked}
- **Data volume for performance:** {approach — generators / subset replication}
- **External dependencies:** {approach — mock / stub / sandbox}

---

## 6. Automation Approach

| Test Type | Automation Level | Rationale |
|-----------|:----------------:|-----------|
| Unit tests | ✅ Fully automated | {reason} |
| Contract tests | ✅ Fully automated | {reason} |
| Integration tests | ✅ Fully automated | {reason} |
| Performance tests | ✅ Automated (scheduled) | {reason} |
| Security tests | 🔶 Partial | {what's automated vs. manual} |
| Acceptance tests | 🔶 Partial | {what's automated vs. manual} |
| Accessibility tests | 🔶 Partial | {what's automated vs. manual} |

### Automation Priority Order

1. Critical-risk tests from debt scorecard
2. Regression-prone areas (high change frequency)
3. Deployment-blocking tests (entry/exit criteria)
4. Tests expensive to run manually (load, cross-browser)

---

## 7. Quality Gates — Entry/Exit Criteria

### Development Entry (before code review)

- [ ] All unit tests pass locally
- [ ] New code has unit tests for new business rules
- [ ] No regression in existing test suite
- [ ] {additional project-specific criteria}

### Integration Entry (before merge to main)

- [ ] Unit + integration tests pass in CI
- [ ] Coverage does not decrease from baseline
- [ ] No Critical-risk debt scorecard items unaddressed for merged code
- [ ] {additional criteria}

### Release Exit (before deployment)

- [ ] All unit + integration + system tests pass
- [ ] Coverage meets targets: Unit ≥ {n}%, Integration ≥ {n}%
- [ ] All Critical-risk items addressed OR accepted with documented rationale
- [ ] No Critical/High severity defects open
- [ ] Performance tests pass SLA targets
- [ ] Security scan clean (no Critical/High vulnerabilities)
- [ ] {additional criteria}

### Sprint Exit

- [ ] Sprint's committed debt scorecard items addressed
- [ ] Coverage trend: improving or stable (not declining)
- [ ] New features have corresponding register entries with Status = Exists
- [ ] {additional criteria}

---

## 8. Test Environments

| Environment | Purpose | Data | Access | Provisioning |
|-------------|---------|------|--------|-------------|
| Local | Unit + integration | In-memory / Docker | Developer | Self-service |
| CI Pipeline | Full automated suite | Ephemeral containers | Automated | Auto on push |
| Staging | System + acceptance | Synthetic production-like | Team | {method} |
| Performance | Load/stress | Scaled synthetic | Scheduled | {method} |

---

## 9. Review Cadence

| Review Type | Frequency | Participants | Focus |
|-------------|:---------:|--------------|-------|
| Coverage report review | {frequency} | {who} | Coverage trends, gap resolution progress |
| Debt scorecard review | {frequency} | {who} | Priority changes, sprint allocation |
| Register reconciliation | When AP changes | QA + Architect | New commitments, deprecated entries |
| Strategy revision | {frequency} | Full team | Goals, tools, process adjustments |

---

## 10. Risks to Test Strategy Execution

| Risk | Mitigation |
|------|-----------|
| Insufficient sprint capacity for test debt | {approach — e.g., reserve 20% sprint capacity for debt} |
| Testing tools break or become unsupported | {approach — e.g., standard choices, community support} |
| Coverage goals conflict with delivery pressure | {approach — e.g., Critical tests are non-negotiable; Medium/Low can slip} |
| Architecture changes faster than tests can keep up | {approach — e.g., reconciliation at each sprint boundary} |

---

*Generated by AI-TGE v{version} | Strategy Phase Stage 5*
