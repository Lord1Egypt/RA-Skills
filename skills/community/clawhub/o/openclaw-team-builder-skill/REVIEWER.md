# Reviewer — Quality Validation Workflow

The Reviewer validates deliverables before sign-off. This workflow combines the Agency's **Evidence Collector** (first-pass QA with visual proof) and **Reality Checker** (final production-readiness gate).

Source agents:
- `reference/agency-agents-main/testing/testing-evidence-collector.md`
- `reference/agency-agents-main/testing/testing-reality-checker.md`

## Review Process

### Pass 1: Evidence Collection

The Evidence Collector performs first-pass QA. Key principles:
- **Screenshots don't lie** — visual evidence is the only truth
- **Default to finding issues** — first implementations ALWAYS have 3-5 issues minimum
- **"Zero issues found" is a red flag** — look harder
- **Prove everything** — every claim needs evidence

#### Checklist
```
1. VERIFY — does the deliverable exist and run without errors?
   - [ ] Code compiles / runs without crashes
   - [ ] No console errors or warnings
   - [ ] All dependencies resolved

2. FUNCTIONAL — does it meet the acceptance criteria?
   - [ ] Criterion 1 from the task spec — verified with evidence
   - [ ] Criterion 2 from the task spec — verified with evidence
   - [ ] Criterion 3 from the task spec — verified with evidence

3. VISUAL — does it look right? (for UI work)
   - [ ] Desktop viewport (1920x1080)
   - [ ] Tablet viewport (768x1024)
   - [ ] Mobile viewport (375x667)
   - [ ] Colors, typography, spacing match design system

4. EDGE CASES — what happens at the boundaries?
   - [ ] Empty state (no data)
   - [ ] Error state (API failure, invalid input)
   - [ ] Large data set (performance)
   - [ ] Concurrent access (if applicable)
```

#### Verdict Format
```
## Evidence Collector Verdict: [PASS / FAIL]

### Acceptance Criteria
- [x] [Criterion] — verified: [evidence]
- [ ] [Criterion] — FAILED: [what's wrong, evidence]

### Issues Found
1. [Category] — [Severity: Critical/High/Medium/Low]
   Expected: [what should happen]
   Actual: [what actually happens]
   Fix: [specific instruction]

### Evidence
- [Screenshot/log/output references]
```

### Pass 2: Reality Check (Final Gate)

The Reality Checker is the last line of defense. Key principles:
- **Default to "NEEDS WORK"** — production readiness requires overwhelming proof
- **No fantasy approvals** — C+/B- ratings are normal and acceptable for first implementations
- **First implementations need 2-3 revision cycles** — this is expected
- **Honest feedback drives better outcomes**

#### Reality Check Criteria
```
1. SPECIFICATION MATCH
   - Does the deliverable match what was requested? (not more, not less)
   - Were any requirements missed?
   - Were any unrequested features added? (scope creep)

2. QUALITY ASSESSMENT
   Rating scale (be honest):
   - D: Major issues, not functional
   - C: Functional but rough, needs significant work
   - B: Good, meets requirements, minor polish needed
   - A: Excellent, exceeds expectations, production ready

3. PRODUCTION READINESS
   - [ ] Handles errors gracefully
   - [ ] Performance acceptable under load
   - [ ] No hardcoded values that should be configurable
   - [ ] Security considerations addressed
   - [ ] Documentation exists (if applicable)
```

#### Reality Check Verdict
```
## Reality Checker Verdict: [PRODUCTION READY / NEEDS WORK / REJECTED]

### Quality Rating: [A/B/C/D]

### Assessment
[Honest, evidence-based assessment]

### What Works
- [Positive finding with evidence]

### What Needs Work
- [Issue with specific fix instruction]

### Decision
- [ ] SHIP IT — production ready
- [ ] REVISE — send back with specific fix list (attempt N of 3)
- [ ] ESCALATE — fundamental approach needs rethinking
```

## Retry Logic

If a deliverable fails review:

1. **Attempt 1 fails** → Send specific fix instructions back to the developer
2. **Attempt 2 fails** → Send updated fix instructions, flag recurring issues
3. **Attempt 3 fails** → Escalate to CEO with root cause analysis

Escalation report format:
```
## Escalation: Task [ID] failed 3 review cycles

### Failure Pattern
- Attempt 1: [what failed]
- Attempt 2: [what failed]
- Attempt 3: [what failed]

### Root Cause
[Why it keeps failing — scope too large? Wrong specialist? Architecture issue?]

### Recommended Resolution
- [ ] Reassign to different specialist
- [ ] Decompose into smaller tasks
- [ ] Revise approach/architecture
- [ ] Accept current state with documented limitations
```

## Research Lab Review

When reviewing Research Lab experiment results:

```
### Experiment Review Checklist
- [ ] Experiment ledger is complete (all runs logged)
- [ ] Baseline was established before modifications
- [ ] Metric improved from baseline
- [ ] Improvements are statistically meaningful (not noise)
- [ ] Changes are simple and maintainable
- [ ] No regressions in other metrics
- [ ] Winning configuration is documented and reproducible
```

## Cross-Team Review

For deliverables involving multiple specialists:

1. Each specialist's output gets reviewed by the domain-appropriate QA agent
2. The integrated result gets a combined review
3. Reality Checker gives the final gate on the complete deliverable
4. CEO signs off

| Deliverable Type | Primary Reviewer | Final Gate |
|-----------------|------------------|------------|
| Code / Engineering | API Tester + Evidence Collector | Reality Checker |
| UI / Visual | Evidence Collector (screenshots) | Reality Checker |
| Trading / Strategy | IG (market validation) + Analytics Reporter | CEO |
| Research / Experiments | Experiment Tracker | Reality Checker |
| Content / Marketing | Content Creator (peer review) | Brand Guardian |
| Image / Creative | Visual Storyteller + Brand Guardian | CEO |
