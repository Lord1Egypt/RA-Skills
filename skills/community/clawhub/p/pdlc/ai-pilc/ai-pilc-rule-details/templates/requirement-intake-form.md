<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Requirement Intake Form

| Field | Value |
|-------|-------|
| **Document** | Requirement Intake Form |
| **Project** | {project_name} |
| **Version** | {version} |
| **Date** | {date} |
| **Status** | _[Draft / Submitted / Accepted]_ |
| **Author** | {requestor_name} |

---

## Section 1: General Information

| Field | Value |
|-------|-------|
| Request ID | {request_id} |
| Date Submitted | {date} |
| Requestor Name | {requestor_name} |
| Requestor Department | {department} |
| Requestor Role/Title | {role_title} |
| Business Unit / Division | {business_unit} |
| Contact Email | {email} |
| Contact Phone | {phone} |

---

## Section 2: Requirement Summary

| Field | Value |
|-------|-------|
| Project/Initiative Name | {project_name} |
| Requirement Title | {requirement_title} |
| Category | ☐ New Capability ☐ Enhancement ☐ Replacement ☐ Brownfield Extension ☐ Compliance ☐ Infrastructure |
| Priority (Requestor View) | ☐ Critical ☐ High ☐ Medium ☐ Low |
| Desired Start Date | {start_date} |
| Desired Completion Date | {completion_date} |

---

## Section 3: Business Need

### Problem Statement

{Description of the current situation, pain points, and why this initiative is needed}

### Expected Business Outcome

- {Outcome 1}
- {Outcome 2}
- {Outcome 3}

### Impact if NOT Addressed

- {Consequence 1}
- {Consequence 2}
- {Consequence 3}

---

## Section 4: Requirements Description

### Functional Requirements

#### {Domain 1}
1. {Requirement statement}
2. {Requirement statement}

#### {Domain 2}
3. {Requirement statement}
4. {Requirement statement}

### Non-Functional Requirements

| Category | Requirement | Target/Metric | Priority |
|----------|------------|---------------|:--------:|
| Performance | {statement} | {target} | {H/M/L} |
| Security | {statement} | {target} | {H/M/L} |
| Scalability | {statement} | {target} | {H/M/L} |
| Availability | {statement} | {target} | {H/M/L} |

### Constraints & Assumptions

**Constraints:**
1. {Hard limit or boundary}
2. {Constraint}

**Assumptions:**
1. {What is assumed true}
2. {Assumption}

---

## Section 5: Existing System Context (Brownfield Only)

> **Include this section IF:** Project Type is "Brownfield Extension" (extending, replacing, integrating with, or modernizing an existing system). **Skip IF:** Pure greenfield with no existing system involvement.

### Existing System Profile

| Field | Value |
|-------|-------|
| Existing System Name | {system_name} |
| Brownfield Type | ☐ Extend (new module) ☐ Replace (subsystem) ☐ Integrate (bidirectional) ☐ Modernize (upgrade) |
| Technology Stack | {language, framework, database, infrastructure} |
| System Age | {years in production} |
| Current State | ☐ Healthy ☐ Aging ☐ Legacy ☐ Critical |
| Documentation | ☐ Well-documented ☐ Partial ☐ Undocumented |
| Test Coverage | ☐ High (>70%) ☐ Moderate (30-70%) ☐ Low (<30%) ☐ None |
| Active Users/Consumers | {who depends on it today} |
| Data Volume | {approximate — rows, storage, growth rate} |
| Team Familiarity | ☐ Expert ☐ Moderate ☐ Limited ☐ None |

### Scope Distinction

| Category | Items |
|----------|-------|
| **EXISTING** (no change) | {Components/features that remain untouched} |
| **CHANGING** (modification) | {Components/features being modified or migrated} |
| **NEW** (additions) | {Components/features being built from scratch} |
| **RETIRING** (decommission) | {Components/features being removed after transition} |

### Coexistence Requirements

| Question | Answer |
|----------|--------|
| Must existing system remain operational during transition? | ☐ Yes (zero downtime) ☐ Yes (planned maintenance windows) ☐ No (can shut down) |
| Parallel operation period? | {estimated duration} |
| Backward compatibility required? | ☐ Yes (all existing APIs/consumers unchanged) ☐ Partial ☐ No |
| Shared database during transition? | ☐ Yes ☐ No ☐ TBD |
| Data migration required? | ☐ Yes (full) ☐ Yes (partial) ☐ No ☐ TBD |
| Feature parity before decommission? | ☐ Full parity ☐ Partial ☐ Not required |

---

## Section 6: Stakeholders & Approvals

| Role | Name | Department |
|------|------|------------|
| Business Sponsor | {name} | {dept} |
| Product Owner | {name} | {dept} |
| Key User/SME | {name} | {dept} |
| Technical Lead | {name} | {dept} |
| Security/Compliance | {name} | {dept} |

---

## Section 7: Preliminary Estimates (if known)

| Field | Value |
|-------|-------|
| Estimated Budget Range | _[TBD]_ |
| Estimated Duration | _[TBD]_ |
| Estimated Team Size | _[TBD]_ |
| Systems/Tools Impacted | {list} |

---

## Section 8: Attachments & References

- [ ] Requirements Document
- [ ] Process Flow Diagrams
- [ ] Architecture Diagrams
- [ ] Current State Assessment
- [ ] Other: {specify}

---

## PMO Use Only

| Field | Value |
|-------|-------|
| Received Date | {date} |
| Assigned Analyst | _[To be assigned]_ |
| Screening Decision | ☐ Proceed ☐ Hold ☐ Reject ☐ More Info Needed |
| Notes | {PMO notes} |

---

*Completed: {date} | Source: {source_reference}*
