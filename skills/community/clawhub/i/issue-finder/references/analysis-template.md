# Issue Analysis Report Template

Use this template for structured issue analysis.

---

## Issue Overview

**Repository**: owner/repo
**Issue Number**: #XXX
**Title**: [Issue Title]
**Type**: Bug / Feature / Enhancement / Documentation
**Created**: YYYY-MM-DD
**Last Updated**: YYYY-MM-DD

---

## Issue Summary

### Description
[One-paragraph summary of what the issue is about]

### Labels
- `label1`
- `label2`

### Current Status
- [ ] Needs triage
- [ ] Confirmed
- [ ] In progress
- [ ] Blocked

---

## Root Cause Analysis (Bug)

### Symptoms
[What the user experiences]

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happens]

### Root Cause
[Technical explanation of why this happens]

### Affected Components
- Component A
- Component B

### Code References
- `file1.ts:line_number` - Description
- `file2.ts:line_number` - Description

---

## Feature Scope (Feature Request)

### Problem Statement
[What problem does this feature solve?]

### Proposed Solution
[What should be implemented?]

### Use Cases
1. [Use case 1]
2. [Use case 2]

### Acceptance Criteria
- [ ] Criteria 1
- [ ] Criteria 2

### Out of Scope
[What this feature will NOT include]

---

## Proposed Approach

### Solution Strategy
1. Step 1
2. Step 2
3. Step 3

### Code Changes Needed
- [ ] File 1: Description of changes
- [ ] File 2: Description of changes
- [ ] New file: Description

### Test Strategy
- [ ] Unit tests for X
- [ ] Integration tests for Y
- [ ] Manual testing steps

---

## Effort Estimation

### Time Estimate
- Research: X hours
- Implementation: Y hours
- Testing: Z hours
- Documentation: W hours
- **Total**: T hours

### Complexity Level
- [ ] Tiny (hours)
- [ ] Small (days)
- [ ] Medium (weeks)
- [ ] Large (weeks-months)

### Files Affected
- Count: N files
- Scope: frontend/backend/both

---

## Risk Assessment

### Technical Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Risk 1 | H/M/L | H/M/L | How to mitigate |

### Breaking Changes
- [ ] No breaking changes
- [ ] Minor breaking changes (describe)
- [ ] Major breaking changes (describe)

### Dependencies
- [ ] No new dependencies
- [ ] New dependencies needed: [list]
- [ ] Dependency version changes: [list]

---

## Learning Opportunities

### Technical Skills
- [ ] New technology/framework
- [ ] Design pattern
- [ ] Testing approach
- [ ] Performance optimization

### Domain Knowledge
- [ ] Business logic
- [ ] Industry standard
- [ ] User experience

### Soft Skills
- [ ] Code review process
- [ ] Technical communication
- [ ] Collaboration

---

## Project Health Check

### Maintainer Engagement
- Response time: X days average
- Last maintainer comment: YYYY-MM-DD
- Assigned to: [maintainer username or "unassigned"]

### Community Activity
- Stars: N
- Contributors: N
- Recent commits: N commits in last 30 days
- Open issues: N
- Open PRs: N

### CI/CD Status
- Tests: ✅ Passing / ❌ Failing
- Build: ✅ Passing / ❌ Failing
- Lint: ✅ Passing / ❌ Failing

---

## Feasibility Scores

### Bug Fix Feasibility
| Criterion | Score (1-10) | Notes |
|-----------|--------------|-------|
| Reproducibility | | |
| Root Cause Clarity | | |
| Scope | | |
| Dependencies | | |
| Test Coverage | | |
| **Average** | | |

### Feature Implementation Feasibility
| Criterion | Score (1-10) | Notes |
|-----------|--------------|-------|
| Requirements Clarity | | |
| Project Alignment | | |
| Implementation Complexity | | |
| Breaking Changes | | |
| Maintainability | | |
| **Average** | | |

### Contribution Value
| Criterion | Score (1-10) | Weight | Weighted |
|-----------|--------------|--------|----------|
| Impact | | 30% | |
| Learning | | 25% | |
| Community | | 20% | |
| Complexity | | 15% | |
| Portfolio | | 10% | |
| **Total** | | 100% | |

---

## Recommendation

### Overall Assessment
- Feasibility Score: X/10
- Value Score: X/10
- Risk Level: Low / Medium / High
- Effort Level: Tiny / Small / Medium / Large

### Decision
- [ ] **PROCEED** - Good opportunity, start work
- [ ] **CONSIDER** - Moderate value, evaluate alternatives
- [ ] **SKIP** - Low ROI or high risk

### Rationale
[Why this recommendation?]

### Next Steps
1. [First action]
2. [Second action]
3. [Third action]

---

## Additional Resources

### Related Issues
- #XXX: Related issue
- #XXX: Similar issue

### Related PRs
- #XXX: Previous attempt
- #XXX: Related PR

### Documentation
- [Link to relevant docs]
- [Link to relevant code section]

---

## Analysis Metadata

**Analyzed by**: [Your username]
**Analysis date**: YYYY-MM-DD
**Analysis version**: 1.0
**Confidence level**: High / Medium / Low