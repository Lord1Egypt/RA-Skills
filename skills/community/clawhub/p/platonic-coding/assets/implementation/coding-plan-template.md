# {{FEATURE_NAME}} Coding Plan

> Coding plan for implementing {{FEATURE_DESCRIPTION}} in {{PROJECT_NAME}}.
>
> **Source Guide**: {{IMPL_GUIDE_PATH}}
> **Source RFC**: {{RFC_PATH}}
> **Language**: {{LANGUAGE}}
> **Framework**: {{FRAMEWORK}}

---

## Summary

{{PLAN_SUMMARY}}

**Total Tasks**: {{TOTAL_TASKS}}
**Estimated Files**: {{ESTIMATED_FILES}} new / {{ESTIMATED_MODIFIED}} modified

---

## Tasks

### Task {{TASK_NUMBER}}: {{TASK_TITLE}}

**Action**: Create / Modify
**File(s)**: `{{FILE_PATH}}`
**Guide Section**: Section {{GUIDE_SECTION}}
**Description**: {{TASK_DESCRIPTION}}

**Deliverables**:
- {{DELIVERABLE_1}}
- {{DELIVERABLE_2}}

**Dependencies**: {{TASK_DEPENDENCIES}}

---

### Task {{TASK_NUMBER}}: Unit Tests for {{COMPONENT}}

**Action**: Create
**File(s)**: `{{TEST_FILE_PATH}}`
**Guide Section**: Section 9.1
**Description**: Unit tests for {{COMPONENT}}

**Test Cases**:
- {{TEST_CASE_1}}
- {{TEST_CASE_2}}
- {{TEST_CASE_3}}

**Dependencies**: Task {{IMPL_TASK_NUMBER}}

---

### Task {{TASK_NUMBER}}: Integration Tests

**Action**: Create
**File(s)**: `{{INTEGRATION_TEST_PATH}}`
**Guide Section**: Section 9.2
**Description**: Integration tests for cross-component behavior

**Test Scenarios**:
- {{SCENARIO_1}}
- {{SCENARIO_2}}

**Dependencies**: {{ALL_IMPL_TASKS}}

---

## Execution Order

1. {{ORDERED_TASK_1}}
2. {{ORDERED_TASK_2}}
3. {{ORDERED_TASK_3}}
...

## Verification Checklist

- [ ] All tasks completed
- [ ] Project builds without errors
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] All RFC requirements covered (see guide Appendix A)
