<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Feasibility Assessment & Prioritization

## Project/Initiative: {project_name}
## Assessed By: {assessor} | Date: {date}
## Request ID: {request_id}

---

## Section 1: Feasibility Dimensions

### Technical Feasibility

| Criteria | Rating (1-5) | Comments |
|----------|:------------:|----------|
| Technology readiness | {n} | {evidence} |
| Integration complexity | {n} | {evidence} |
| Infrastructure availability | {n} | {evidence} |
| Skills/expertise available | {n} | {evidence} |
| **Technical Score** | **{sum}/20** | {summary} |

### Operational Feasibility

| Criteria | Rating (1-5) | Comments |
|----------|:------------:|----------|
| Process change impact | {n} | {evidence} |
| User adoption risk | {n} | {evidence} |
| Organizational readiness | {n} | {evidence} |
| Training requirements | {n} | {evidence} |
| **Operational Score** | **{sum}/20** | {summary} |

### Financial Feasibility

| Criteria | Rating (1-5) | Comments |
|----------|:------------:|----------|
| Budget availability | {n} | {evidence} |
| ROI potential | {n} | {evidence} |
| Cost certainty | {n} | {evidence} |
| Funding approval likelihood | {n} | {evidence} |
| **Financial Score** | **{sum}/20** | {summary} |

### Schedule Feasibility

| Criteria | Rating (1-5) | Comments |
|----------|:------------:|----------|
| Timeline realism | {n} | {evidence} |
| Resource availability timing | {n} | {evidence} |
| Dependency alignment | {n} | {evidence} |
| Regulatory/compliance deadlines | {n} | {evidence} |
| **Schedule Score** | **{sum}/20** | {summary} |

### Integration Feasibility (Brownfield Only)

> **Include IF:** Project Type is "Brownfield Extension". **Skip IF:** Pure greenfield.

| Criteria | Rating (1-5) | Comments |
|----------|:------------:|----------|
| Existing system stability for integration | {n} | {evidence — is the existing system stable enough to integrate with?} |
| API/interface availability | {n} | {evidence — does the existing system expose usable interfaces?} |
| Data migration complexity | {n} | {evidence — how complex is moving/sharing data?} |
| Backward compatibility achievability | {n} | {evidence — can we maintain compatibility with existing consumers?} |
| **Integration Score** | **{sum}/20** | {summary} |

> **Scoring note (brownfield):** When Integration Feasibility is included, the overall weighting adjusts to: Technical 25% + Operational 20% + Financial 20% + Schedule 15% + Integration 20% = 100%.

---

## Section 2: Overall Feasibility Score

| Dimension | Score | Weight | Weighted Score |
|-----------|:-----:|:------:|:--------------:|
| Technical | {x}/20 | 30% | {weighted} |
| Operational | {x}/20 | 25% | {weighted} |
| Financial | {x}/20 | 25% | {weighted} |
| Schedule | {x}/20 | 20% | {weighted} |
| **Total Weighted Score** | | | **{total}/100** |

### Feasibility Rating: {🟢🟡🟠🔴} {Rating Name}

**Assessment:** {Summary statement interpreting the score and identifying key areas of concern}

---

## Section 3: Prioritization

### Strategic Alignment Score

| Criteria | Rating (1-5) | Comments |
|----------|:------------:|----------|
| Alignment to business strategy | {n} | {evidence} |
| Revenue/cost impact | {n} | {evidence} |
| Customer/user impact | {n} | {evidence} |
| Regulatory/compliance need | {n} | {evidence} |
| Competitive advantage | {n} | {evidence} |
| **Strategic Score** | **{sum}/25** | {summary} |

### Priority Classification

| Method | Result |
|--------|--------|
| MoSCoW Category | ☐ Must Have ☐ Should Have ☐ Could Have ☐ Won't Have |
| Value Score (1-10) | **{n}** |
| Effort Score (1-10) | **{n}** |
| Value/Effort Ratio | **{ratio}** |
| Final Priority Rank | **{Pn} — {label}** |

**Rationale:** {Why this priority was assigned}

---

## Section 4: Conditions for Proceeding

| # | Condition | Owner | Target Date | Blocking? |
|---|-----------|-------|:-----------:|:---------:|
| 1 | {condition} | {owner} | {date} | {Yes/No} |

---

## Section 5: Recommendation

| Field | Value |
|-------|-------|
| Recommendation | ☐ Approve ☐ Approve with Conditions ☐ Hold ☐ Reject |
| Conditions | {If applicable} |
| Assessed By | {name/role} |
| Assessment Date | {date} |
| Approved By | _[Pending]_ |

### Summary Statement

{2-3 sentence summary of feasibility, priority, and recommendation}

---

*Completed: {date} | Next Phase: {next_phase}*
