# Technical Due Diligence

## Objectives

Conduct a comprehensive technical assessment of the target company / system / product, identifying technical risks, technical debt, architecture quality, and team capability. Produce a Technical Due Diligence Report to support investment / M&A / partnership decisions.

---

## Prerequisites
- Due diligence scope has been defined (full scope / specific systems / specific teams)
- Target party has signed NDA and granted data access
- Due diligence team has been assembled (requires architecture / security / data / development roles)

## Inputs
- Due Diligence Scope Statement (Scope of DD)
- Technical documentation checklist provided by the target party
- Data access permissions (code repositories / systems / monitoring / logs)
- Due diligence questionnaire has been sent

---

## Operation Steps

### Step 1: Due Diligence Preparation

#### 1.1 Document Request Checklist (DD Request List)

Document request checklist to send to the target party:

```
□ Architecture Documentation:
  - System architecture diagrams (logical + physical)
  - Data architecture diagrams / data flow diagrams
  - Integration / interface documentation
  - Technology selection decision records (ADR)

□ Code & Engineering:
  - Code repository access
  - CI/CD process documentation
  - Code quality scan reports
  - Test strategy & coverage reports

□ Infrastructure:
  - Infrastructure topology diagrams
  - Cloud resource inventory (including billing)
  - Monitoring & alerting configuration
  - BCP/DR documentation + drill records

□ Security:
  - Security architecture documentation
  - Penetration test reports (last 2 rounds)
  - Security incident records (past 2 years)
  - Compliance certifications (ISO 27001 / SOC2 / Information Security Classified Protection)

□ Team:
  - Technical team organization chart
  - Key personnel resumes (can be anonymized)
  - Attrition rate (past 2 years)
  - Outsourcing / vendor dependency list

□ Product:
  - Product feature list with technical mapping
  - Known technical defects / Bug Backlog
  - Product roadmap (technical perspective)
  - Third-party dependency list (open-source + commercial)
```

#### 1.2 Due Diligence Team Role Assignment

| Role | Scope of Responsibility | Estimated Effort (Days) |
|------|------------------------|--------------------------|
| DD Lead | Overall coordination + synthesis report | 5-10 |
| Architecture Assessor | Architecture quality + scalability | 3-7 |
| Security Assessor | Security posture + compliance | 3-5 |
| Data Assessor | Data architecture + data quality | 2-4 |
| Engineering Assessor | Code quality + engineering practices | 3-5 |
| DevOps Assessor | Infrastructure + operations maturity | 2-4 |

---

### Step 2: Architecture Assessment (Dimension 1 of the Bain Tech DD Five-Dimension Framework)

#### 2.0 Bain Tech DD Five-Dimension Framework Overview
Before entering specific assessments, first confirm that the due diligence covers all five dimensions (see details in references/core-methodology-library.md §14):

| Dimension | Weight | Check Items | Core Method | Output |
|-----------|--------|-------------|-------------|--------|
| **Architecture Quality** | 25% | 20+ | Architecture review + ADR analysis + dependency scanning | Architecture score + technical debt quantification |
| **Engineering Practices** | 20% | 25+ | Code review + CI/CD + DORA metrics | Engineering maturity score |
| **Security Posture** | 20% | 20+ | Penetration testing + vulnerability scanning + compliance review | Security risk matrix |
| **Data Quality** | 15% | 15+ | Data model review + data pipeline analysis | Data debt quantification |
| **Team Capability** | 20% | 20+ | Key-person interviews + Bus Factor analysis | Team risk matrix |

> **Bain Methodology Core**: Due diligence is not about finding fault — it's about quantifying risk. "This system has problems" → "$0.5M + 6 months to remediate, valuation should be adjusted down by $0.3M."
> Valuation Impact Quantification: Total Technical Debt = Σ (remediation cost per debt category) × Risk Coefficient → Recommended Valuation Adjustment

### Step 2: Architecture Assessment

#### 2.1 Architecture Quality Scoring

| Dimension | Score (1-5) | Assessment Question |
|-----------|-------------|---------------------|
| Modularity | [1-5] | Are system boundaries clear? How is the coupling? |
| Scalability | [1-5] | How much rework is needed to support 3-5x user growth? |
| Maintainability | [1-5] | How long does it take a new hire to understand and modify the code? |
| Fault Isolation | [1-5] | If one module fails, does it affect others? |
| Performance Design | [1-5] | Are there performance bottlenecks? Caching / Async / Queues? |
| Security Design | [1-5] | Is security bolted on or natively integrated into the architecture? |

#### 2.2 Technical Debt Quantification

| Debt Type | Identification Method | Severity (L/M/H) | Estimated Remediation Cost |
|-----------|----------------------|------------------|----------------------------|
| Architecture Debt | Circular dependencies between modules, no documentation, lost key design decisions | H | $0.5-2M |
| Code Debt | Code duplication >10%, test coverage <30%, no coding standards | M | $0.2-0.5M |
| Infrastructure Debt | No IaC, manual deployment, no monitoring, no disaster recovery | H | $0.3-1M |
| Security Debt | Known vulnerabilities unpatched >90 days, no penetration testing, outdated authentication | H | $0.2-1M |
| Data Debt | Chaotic data model, no data dictionary, fully manual ETL | M | $0.3-0.8M |
| Dependency Debt | Using EoL versions of frameworks/libraries, unmaintained internal libraries | H | $0.5-1.5M |

**Total Estimated Technical Debt: $[X]M**
**Remediation Time: [X] months, requiring [X] people**

#### 2.3 Open-Source Dependency Risk

| Risk | Inspection Method | Example |
|------|-------------------|---------|
| License Risk | Scan all dependency licenses | GPLv3 in a commercial closed-source product → litigation risk |
| Security Vulnerabilities | OWASP Dependency Check | Log4j / CVSS >9 unpatched vulnerabilities |
| Maintenance Activity | GitHub stars / issues / commit frequency | Last commit was 2 years ago → likely abandoned |
| Critical Library Single-Point Dependency | Identify irreplaceable critical dependencies | "The entire messaging system depends on this library maintained by a single person" |

---

### Step 3: Engineering Practices Assessment

#### 3.1 Code Quality

**Sampling Method**: Select 3-5 core modules, ~1,000 lines of code each for review

| Metric | Target | Actual | Assessment |
|--------|--------|--------|-------------|
| Test Coverage | >70% | [%] | [Green / Yellow / Red] |
| Code Duplication Rate | <5% | [%] | [Green / Yellow / Red] |
| Cyclomatic Complexity (Avg) | <10 | [X] | [Green / Yellow / Red] |
| Coding Standard Consistency | High | [High / Medium / Low] | [Green / Yellow / Red] |
| Code Review Rate | >90% | [%] | [Green / Yellow / Red] |

#### 3.2 CI/CD Maturity

```
□ Auto-trigger build on code commit?   Yes / No
□ Automated tests run in CI?           Yes / No
□ Is deployment automated?             Yes / No
□ Is there a pre-production environment for verification? Yes / No
□ Deployment frequency?                [X times / day / week / month]
□ Average time from Commit to Production? [X days]
□ One-click rollback supported?        Yes / No
□ Change failure rate?                 [X%]
```

#### 3.3 Core Engineering Risk Assessment

| Risk | Impact | Likelihood | Level |
|------|--------|------------|-------|
| Key-person dependency ("Only Old Li knows") | High | Medium | 🔴 |
| No automated tests, relies on manual regression | High | High | 🔴 |
| No disaster recovery drills, DR plan exists only in PPT | High | Medium | 🟡 |
| Manual deployment, documentation outdated | Medium | High | 🟡 |

---

### Step 4: Team Assessment

#### 4.1 Team Structure Analysis

| Role | Headcount | Avg Tenure | Assessment |
|------|-----------|------------|-------------|
| Architect | [X] | [Y years] | Sufficient / Insufficient / Excess |
| Backend Developer | [X] | [Y years] | ... |
| Frontend / Mobile | [X] | [Y years] | ... |
| Data Engineer | [X] | [Y years] | ... |
| DevOps / SRE | [X] | [Y years] | ... |
| QA / Test | [X] | [Y years] | ... |
| Security Engineer | [X] | [Y years] | ... |

**Ratio Analysis:**
- Dev : QA = [X:1] (Industry benchmark: 3:1 ~ 5:1)
- Dev : DevOps = [X:1] (Industry benchmark: 5:1 ~ 10:1)
- Senior : Junior = [X:1] (Healthy team: 1:2 ~ 1:3)

#### 4.2 Key-Person Dependencies

| Name (can be anonymized) | Critical Knowledge / System Owned | Impact if Departed | Succession Plan |
|--------------------------|-----------------------------------|--------------------|-----------------|
| Employee A | Core transaction logic, only they understand it | Transaction system unable to iterate for 2-3 months | No succession plan ⚠️ |
| Employee B | Full picture of data pipelines | Data delays, 1-2 month transition needed | Documentation + deputy available |
| ... |

#### 4.3 Team Culture Indicators

```
□ Do engineers see themselves as "cogs" or "owners"?
□ After an incident, is it "who is responsible" or "how to prevent recurrence"?
□ Are technical decisions top-down or team consensus?
□ Is there a culture and budget for continuous learning?
□ How often do engineers change jobs on average? (External data: LinkedIn)
```

---

### Step 5: Security Due Diligence

#### 5.1 Security Quick Assessment

| Check Item | Finding | Risk |
|------------|---------|------|
| Have all internet-facing systems undergone penetration testing? | | |
| Does authentication support MFA? | | |
| Is production data isolated from non-production environments? | | |
| Are third-party / vendor security assessments conducted? | | |
| Is there a security incident response process (and has it been tested)? | | |
| Is critical data encrypted (in transit + at rest)? | | |
| Have there been any security incidents in the past 12 months? | | |
| Do developers have access to production data? | | |
| Are there hardcoded secrets / passwords in code repositories? | | |
| Has security training + phishing testing been conducted? | | |

#### 5.2 Security Red / Yellow / Green Flags

```
🔴 Red Flags (Potential Deal Breaker):
- Customer data breach in the past 12 months with no corrective actions taken
- Core systems with no authentication or default passwords
- Known critical vulnerabilities (CVSS >9) unpatched for over 90 days
- All required compliance certifications missing

🟡 Yellow Flags (Remediation Needed):
- Security tools purchased but not fully deployed
- Understaffed security team (e.g., 2 people for a 2,000-person company)
- Security awareness training missing
- DR plan exists but has never been tested

🟢 Green Flags:
- Security embedded in the development process (Shift Left Security)
- Regular penetration testing + red team exercises
- Full set of security certifications maintained and current
- Security team has a reporting line to the board level
```

---

### Step 6: Synthesis Assessment & Report

#### 6.1 Due Diligence Conclusion Framework

```
Overall Technical Assessment: [Strong / Moderate / Weak / High Risk]

Key Findings (Top 5):
1. [Finding] → Impact: [$X] → Recommendation: [...]
2. ...

If Acquisition / Partnership:
├── Additional investment required post-integration: $[X]M (technical debt remediation + platform integration + security hardening)
├── Integration timeline: [X] months
├── Key Integration Risks:
│   ├── Risk 1: [Personnel attrition / Technology incompatibility / Data migration / ...]
│   └── Risk 2: [...]
└── Alternative: [If this deal is not done, building in-house would cost $[X]M + [X] months]

Valuation Impact:
├── Technical debt deduction: $[X]M
├── Security hardening deduction: $[X]M
├── Team strengthening deduction: $[X]M
└── Recommended valuation adjustment: -$[X]M (Explanation: Valuation reduction due to technical factors)
```

#### 6.2 Due Diligence Report Structure

1. Executive Summary (1 page: Key findings + Recommendations + Valuation impact)
2. Assessment Scope & Methodology
3. Architecture Assessment
4. Engineering Practices Assessment
5. Security Assessment
6. Team Assessment
7. Technical Debt Quantification
8. Integration / Migration Risks
9. Conclusions & Recommendations
10. Appendix (Detailed scores + Raw data)---

## Outputs
1. **Document Request Checklist** (sent to target party)
2. **Technical Due Diligence Scorecard** (scores across all dimensions)
3. **Technical Debt Quantification Table** (including remediation costs)
4. **Key Risk Register** (including mitigation recommendations)
5. **Technical Due Diligence Report** (full version, per the structure above)
6. **Valuation Impact Analysis** (if applicable)

---

## Quality Checklist
- [ ] All scores are backed by objective evidence, not "I think so"
- [ ] Technical debt has quantified dollar amounts, not "a lot" or "a bit messy"
- [ ] Key-person dependencies have been identified with risk levels
- [ ] Security assessment covers the "crown jewel" assets
- [ ] Report contains actionable recommendations with priorities
- [ ] Risks outside the DD scope are also noted ("The following items were not within the scope of this DD and are recommended for future attention...")

---

## Common Pitfalls

| Pitfall | Why It's Wrong | Correct Approach |
|---------|---------------|------------------|
| Looking only at PPT and documentation | The target's architecture PPT typically shows systems 3x healthier than reality | Look at code → Look at monitoring → Look at logs → Look at Bug Tracker |
| Ignoring team quality | Code can be changed, but a toxic team culture / key-person attrition can destroy everything | Spend at least 30% of effort assessing team and culture |
| Listing problems without solutions | "The architecture is terrible" → useless for decision-making | "The architecture has X/Y/Z problems; remediation requires $A + B person-months; valuation should be adjusted down by $C accordingly" |
| Due diligence team only finds fault | No system in the world is perfect; the purpose of DD is not to prove how smart you are | Distinguish "fatal issues" from "imperfect but acceptable" |
| Ignoring non-functional requirements | QPS / Latency / Availability / SLA — actual production performance matters more than code quality | Always review production monitoring data (at least the past 30 days) |