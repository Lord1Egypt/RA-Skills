<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Test Strategy Generation

## Stage: 5 of 12
## Phase: 🔵 STRATEGY
## Execution: ALWAYS

---

## Purpose

Using the test register (Stage 3), brownfield assessment (Stage 4, if applicable), tech stack context (from DW), and depth level, produce a comprehensive **Test Strategy** document. This strategy defines the testing approach, pyramid ratios, tool selection, coverage goals, test data strategy, automation approach, and entry/exit criteria for the project.

The strategy is derived — not invented. It flows from what the architecture requires and what the workspace provides.

---

## Depth Adaptation

| Depth | Strategy Scope | Document Length |
|-------|---------------|:---------------:|
| **Minimal** | Test pyramid ratios + tool list + coverage goals + entry/exit criteria. No test data strategy. No automation roadmap. 1-2 pages. | Short |
| **Standard** | All strategy sections: pyramid, tools, coverage goals, test data strategy, automation approach, entry/exit criteria, environment needs. 3-5 pages. | Medium |
| **Comprehensive** | All Standard sections + detailed automation roadmap + environment provisioning plan + test data lifecycle + cross-team testing coordination + quality gate definitions per phase. 5-8 pages. | Full |

---

## MANDATORY: Stage Sub-Role — Process Designer

During THIS stage, ALSO adopt the mindset of a **Process Designer**. This does NOT replace your primary role (Senior QA Engineer / Test Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Design the testing PROCESS, not just list what to test — think about flow, sequence, and dependencies
- Base tool recommendations on what the workspace ALREADY provides (DW tech stack) — don't introduce new tools unless necessary
- Define measurable targets, not aspirations: "80% unit coverage" not "high coverage"
- Think about repeatability: can this strategy be executed consistently sprint after sprint?

### Anti-Patterns for This Stage
- Do NOT recommend tools not present in the workspace's tech stack without explicit justification
- Do NOT set unrealistic coverage targets (99% coverage on day 1 for a brownfield project = wrong)
- Do NOT produce a generic strategy that could apply to any project — it must reference THIS project's register and architecture
- Do NOT skip entry/exit criteria — without gates, the strategy is unenforceable

### Quality Check
A good output at this stage sounds like:
- "Test Strategy: pyramid ratio 50/25/15/10 (based on 67 register entries with heavy business logic). Jest + Supertest for unit/integration (already in DW). Coverage target: 80% unit, 60% integration (brownfield — current is 45%, so target is incremental). Entry criteria: feature branch passes lint + unit tests. Exit: all Critical-risk tests from debt scorecard pass before release."

---

## Step-by-Step Execution

### Step 1: Load Context

Gather inputs for strategy derivation:

| Input | Source | What It Provides |
|-------|--------|-----------------|
| Test Register | Stage 3 output (`.governance/test/test-register.md`) | What tests are needed, their levels and types |
| Brownfield Gap Map | Stage 4 output (if exists) | Current coverage baseline (what's already done) |
| Tech Stack | DW `rules/tech-stack.md` | Available testing frameworks, languages, tools |
| Testing Conventions | DW `rules/testing-strategy.md` (if exists) | Team's existing testing approach |
| Module Structure | DW `rules/module-structure.md` (if exists) | Boundaries that define test scopes |
| Depth Level | State file | How detailed the strategy should be |

---

### Step 2: Determine Test Pyramid Ratios

Calculate recommended pyramid ratios based on register composition:

**Default targets (from test-taxonomy.md):**

| Depth Level | Unit | Integration | System | Acceptance |
|-------------|:----:|:-----------:|:------:|:----------:|
| Minimal | 60% | 25% | 10% | 5% |
| Standard | 50% | 25% | 15% | 10% |
| Comprehensive | 40% | 30% | 20% | 10% |

**Adjustments based on architecture:**

| Project Characteristic | Adjustment |
|-----------------------|-----------|
| Heavy API / microservices | ↑ Integration (more contracts to verify) |
| Complex business logic | ↑ Unit (more rules to isolate) |
| Many user workflows | ↑ Acceptance (more end-to-end flows) |
| High security surface | ↑ System (security tests need full stack) |
| Few integrations, simple CRUD | ↑ Unit, ↓ Integration |
| Brownfield with low existing coverage | Start conservative; ramp incrementally |

**Present as:**
```markdown
## Recommended Test Pyramid

| Level | Target % | Rationale |
|-------|:--------:|-----------|
| Unit | {n}% | {why — based on register distribution} |
| Integration | {n}% | {why} |
| System | {n}% | {why} |
| Acceptance | {n}% | {why} |
```

---

### Step 3: Select Testing Tools and Frameworks

Derive tool recommendations from DW tech stack:

| Tech Stack Element | Testing Tool | Role |
|-------------------|-------------|------|
| Language: TypeScript/JavaScript | Jest / Vitest | Unit + Integration |
| Language: Python | Pytest | Unit + Integration |
| Language: Go | Built-in `testing` package | Unit + Integration |
| Language: Java | JUnit 5 + Mockito | Unit + Integration |
| API Framework: Express/Fastify | Supertest | API contract tests |
| API Framework: FastAPI | httpx / TestClient | API contract tests |
| Frontend: React/Vue/Angular | Testing Library + Playwright | Component + E2E |
| Database: SQL | In-memory DB / testcontainers | Data integrity tests |
| External Services | WireMock / nock / responses | Integration mocking |
| Performance | k6 / Artillery / Locust | Load/performance tests |
| Coverage | Istanbul (nyc) / coverage.py / go cover | Coverage measurement |

**Rules:**
- Use what the DW already has configured — don't add dependencies unnecessarily
- If DW has no testing framework, recommend the standard choice for the language
- If multiple options exist, prefer the one already in `package.json` / `requirements.txt` / `go.mod`

---

### Step 4: Define Coverage Goals

Set measurable targets per level:

```markdown
## Coverage Goals

| Level | Target | Measurement | Rationale |
|-------|:------:|-------------|-----------|
| Unit | {n}% branch coverage | Istanbul / coverage.py | {why this target — based on complexity and current state} |
| Integration | {n}% of integration register entries | Register status tracking | {why} |
| System | {n}% of system register entries | Register status tracking | {why} |
| Acceptance | {n}% of acceptance criteria covered | Register status tracking | {why} |
```

**Brownfield adjustment:** If current coverage is known (from Stage 4), set incremental targets:
- Current: 35% → Sprint target: 45% → Release target: 60% → Mature target: 80%
- Never set 100% as an immediate target for brownfield — it's unrealistic and demoralizing

---

### Step 5: Define Test Data Strategy (Standard+ Depth)

```markdown
## Test Data Strategy

### Approach
{Describe how test data is created, managed, and cleaned up for this project}

### By Test Level

| Level | Data Strategy | Isolation |
|-------|--------------|-----------|
| Unit | In-memory fixtures / factories | Complete isolation — no external state |
| Integration | Test database (seeded per suite) | Isolated per test suite; reset between runs |
| System | Staging environment with synthetic data | Shared environment; careful state management |
| Acceptance | Scenario-specific data setup | Created per scenario; cleaned up after |

### Data Considerations
- Sensitive data: {approach — synthetic only / anonymized / etc.}
- Data volume: {approach for performance tests — generators / replicated subsets}
- External dependencies: {mock / stub / sandbox environment}
```

---

### Step 6: Define Automation Approach (Standard+ Depth)

```markdown
## Automation Approach

### Automated vs. Manual

| Test Type | Automation | Rationale |
|-----------|:----------:|-----------|
| Unit tests | ✅ Fully automated | Fast, repeatable, no human judgment needed |
| Contract tests | ✅ Fully automated | Schema validation is deterministic |
| Integration tests | ✅ Fully automated | External mocking makes them reliable |
| Performance tests | ✅ Automated (scheduled) | Require consistent load generation |
| Security tests | 🔶 Partially automated | Static analysis automated; penetration testing manual |
| Acceptance tests | 🔶 Partially automated | Happy paths automated; exploratory manual |
| Accessibility tests | 🔶 Partially automated | Axe/Lighthouse automated; assistive tech manual |
| Usability tests | ❌ Manual only | Requires human judgment |

### Automation Priority (what to automate first)
1. Critical-risk tests from debt scorecard (highest risk if untested)
2. Regression-prone areas (components that change frequently)
3. Tests that block deployment (entry/exit criteria tests)
4. Tests that are expensive to run manually (load tests, cross-browser)
```

---

### Step 7: Define Entry/Exit Criteria

```markdown
## Quality Gates — Entry/Exit Criteria

### Development Entry Criteria (before code review)
- [ ] All unit tests pass locally
- [ ] New code has unit tests for new business rules
- [ ] No regression in existing test suite

### Integration Entry Criteria (before merge to main)
- [ ] Unit + integration tests pass in CI
- [ ] Coverage does not decrease from baseline
- [ ] No Critical-risk tests from debt scorecard remain unaddressed for merged code

### Release Exit Criteria (before deployment)
- [ ] All unit + integration + system tests pass
- [ ] Coverage meets target: Unit ≥ {n}%, Integration ≥ {n}%
- [ ] All Critical-risk debt scorecard items addressed OR accepted with rationale
- [ ] No Critical/High severity defects open
- [ ] Performance tests pass stated SLA targets
- [ ] Security scan clean (no Critical/High vulnerabilities)

### Sprint Exit Criteria (end of sprint)
- [ ] Sprint's committed test debt addressed (from debt scorecard)
- [ ] Coverage trend: improving or stable (not declining)
- [ ] New register entries from sprint's features have Status = Exists
```

---

### Step 8: Define Environment Requirements (Comprehensive Depth Only)

```markdown
## Test Environments

| Environment | Purpose | Data | Access |
|-------------|---------|------|--------|
| Local (developer) | Unit + integration tests | In-memory / Docker | Individual developer |
| CI (pipeline) | Full automated suite | Ephemeral containers | Automated only |
| Staging | System + acceptance tests | Synthetic production-like | Team access |
| Performance | Load/stress testing | Scaled synthetic data | Scheduled runs |
```

---

### Step 9: Compile Test Strategy Document

Assemble all sections into the strategy template:

```markdown
# Test Strategy

**Type:** Strategy
**Generated:** {ISO timestamp}
**Engine:** AI-TGE v1.0.0
**Mode:** {mode}
**Depth:** {depth level}
**Project:** {project_name}

## 1. Overview
{Brief: what this strategy governs, how many test requirements exist, key architectural characteristics}

## 2. Test Pyramid
{From Step 2}

## 3. Testing Tools & Frameworks
{From Step 3}

## 4. Coverage Goals
{From Step 4}

## 5. Test Data Strategy
{From Step 5 — Standard+ only}

## 6. Automation Approach
{From Step 6 — Standard+ only}

## 7. Entry/Exit Criteria
{From Step 7}

## 8. Environment Requirements
{From Step 8 — Comprehensive only}

## 9. Review Cadence
- Coverage report: {frequency — weekly / per-sprint / per-release}
- Debt scorecard review: {frequency}
- Register reconciliation: {when AP changes}
- Strategy revision: {quarterly / per-major-release}
```

---

### Step 10: Present for Review

```markdown
## Review: Test Strategy

I've produced the Test Strategy based on your register ({N} test requirements) and workspace ({framework} configured).

**Key decisions in this strategy:**
- Pyramid: {ratios} — {brief rationale}
- Tools: {primary tools} (from your workspace)
- Coverage target: {target} ({"greenfield ambitious" / "brownfield incremental from current {n}%"})
- Automation: {n}% automated, {n}% manual
- Gates: {key entry/exit criteria highlight}

**Full strategy saved to:** `.governance/test/test-strategy.md`

---

**Your response:**
- (a) **Approve** — strategy aligns with our approach; proceed to risk scoring
- (b) **Adjust targets** — coverage goals or pyramid ratios need changing
- (c) **Change tools** — we prefer different testing tools (specify)
- (d) **Modify gates** — entry/exit criteria are too strict/lenient
- (e) **Add considerations** — there are testing constraints not captured
```

---

## Gate

**This stage has a GATE.** The test strategy defines HOW the team approaches testing. If the team disagrees with tool choices, coverage targets, or entry/exit criteria, that must be resolved before risk scoring — otherwise debt priorities will be misaligned.

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Test Strategy | `.governance/test/test-strategy.md` | Defines testing approach for the project |
| Updated state file | `.governance/test/tge-state.md` | Stage 5 complete |

---

## Stage Completion Criteria

| Check | Pass Criteria |
|-------|---------------|
| Pyramid ratios defined | Percentages sum to 100%; aligned with register distribution |
| Tools from workspace | Testing tools reference actual DW tech stack (not invented) |
| Coverage goals measurable | Specific numbers, not vague ("≥80%" not "good coverage") |
| Entry/exit criteria defined | At least: dev entry, merge entry, release exit |
| Brownfield-aware targets | If brownfield, targets are incremental from current state |
| Automation approach stated | Which tests are automated vs. manual (with rationale) |
| User approved | Strategy confirmed as acceptable approach |
| State file updated | Stage 5 = complete |
