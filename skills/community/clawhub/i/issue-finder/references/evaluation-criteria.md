# Issue Evaluation Criteria

Detailed framework for assessing GitHub issues for contribution value.

## Bug Fix Assessment

### Reproducibility Check

**High Reproducibility** (Score: 9-10):
- Clear step-by-step reproduction instructions
- Includes environment details (OS, version, config)
- Minimal reproduction case provided
- Screenshots/logs attached

**Medium Reproducibility** (Score: 5-8):
- General description of issue
- Some environment context
- Needs investigation to reproduce

**Low Reproducibility** (Score: 1-4):
- Vague description
- Missing environment details
- Cannot reproduce with provided info

### Root Cause Complexity

**Simple** (Score: 9-10):
- Single function/method affected
- Clear cause from error message/stack trace
- Logic error, typo, or missing null check

**Moderate** (Score: 5-8):
- Multiple files/components involved
- Requires understanding of module interaction
- May need debugging or logging

**Complex** (Score: 1-4):
- Architectural or design-level issue
- Multiple systems affected
- Requires deep domain knowledge

### Fix Scope Analysis

| Scope | Files | Risk | Effort |
|-------|-------|------|--------|
| Tiny | 1 | Low | Hours |
| Small | 1-3 | Low-Medium | Days |
| Medium | 3-10 | Medium | Weeks |
| Large | 10+ | High | Weeks-Months |

### Dependency Impact

**Low Impact**:
- No external dependency changes
- Internal changes only
- Backward compatible

**Medium Impact**:
- Version bumps needed
- API changes within module
- Some breaking changes

**High Impact**:
- Major dependency updates
- Breaking API changes
- Requires migration path

## Feature Implementation Assessment

### Clarity of Requirements

**Clear Requirements** (Score: 9-10):
- Detailed specification
- Acceptance criteria defined
- Mockups or examples provided
- Use cases documented

**Moderate Clarity** (Score: 5-8):
- General idea described
- Some requirements implied
- Needs design discussion

**Unclear Requirements** (Score: 1-4):
- Vague feature request
- No acceptance criteria
- Requires significant design work

### Alignment with Project

**High Alignment**:
- Fits project's stated goals
- Maintainers have expressed interest
- Similar features exist

**Medium Alignment**:
- Reasonable extension
- May need discussion
- Some maintainer interest

**Low Alignment**:
- Niche use case
- Diverges from project vision
- No maintainer interest shown

### Implementation Complexity

**New Code Path** (easier):
- Adding new function/module
- Minimal changes to existing code
- Clear extension points

**Modifying Existing Code** (harder):
- Refactoring needed
- Breaking changes possible
- Must understand existing patterns

### Breaking Change Risk

**No Breaking Changes**:
- Additive only
- New optional features
- Backward compatible

**Minor Breaking Changes**:
- Deprecation needed
- Migration guide required
- Version bump required

**Major Breaking Changes**:
- API rewrites
- Data migration needed
- Significant user impact

## Project Health Indicators

### Maintainer Responsiveness

| Response Time | Score |
|---------------|-------|
| < 24 hours | 10 |
| 1-3 days | 8 |
| 3-7 days | 6 |
| 1-2 weeks | 4 |
| 2-4 weeks | 2 |
| > 1 month | 1 |

### Community Activity

**Active Community** (Score: 9-10):
- Multiple active contributors
- Regular PR reviews
- Recent releases
- Active discussions

**Moderate Activity** (Score: 5-8):
- Some contributors active
- Occasional reviews
- Releases every few months
- Some discussions

**Low Activity** (Score: 1-4):
- Few active contributors
- Slow/no reviews
- No recent releases
- Stale discussions

### Documentation Quality

**Excellent**:
- Clear contributing guidelines
- Well-documented codebase
- Active wiki/docs
- Good code comments

**Adequate**:
- Basic contributing docs
- Some code documentation
- Acceptable comments

**Poor**:
- Missing contributing guidelines
- Undocumented code
- Sparse comments

## Risk Assessment Matrix

### Technical Risk

| Risk Level | Indicators | Mitigation |
|------------|------------|------------|
| Low | Simple fix, well-understood, existing tests | None needed |
| Medium | Moderate complexity, some unknowns | Extra testing, maintainer guidance |
| High | Complex, many unknowns, no tests | Spike/POC first, maintain close coordination |

### Time Risk

| Risk Level | Indicators | Mitigation |
|------------|------------|------------|
| Low | Clear scope, familiar tech stack | Time buffer 10-20% |
| Medium | Some unknowns, partial familiarity | Time buffer 30-50% |
| High | Many unknowns, unfamiliar stack | Time buffer 50-100%, consider spike |

### Social Risk

| Risk Level | Indicators | Mitigation |
|------------|------------|------------|
| Low | Responsive maintainers, active community | Standard communication |
| Medium | Somewhat responsive, moderate activity | Regular updates, ask questions early |
| High | Unresponsive, inactive or toxic community | Consider alternative projects |

## Decision Matrix

### When to Proceed

- Feasibility score ≥ 6
- Value score ≥ 7
- Project health score ≥ 6
- All risks manageable
- Time investment acceptable

### When to Consider Carefully

- Feasibility score 4-5
- Value score 5-6
- Project health score 4-5
- Some risks concerning
- Consider partial approach

### When to Skip

- Feasibility score < 4
- Value score < 5
- Project health score < 4
- High risks
- Better alternatives exist