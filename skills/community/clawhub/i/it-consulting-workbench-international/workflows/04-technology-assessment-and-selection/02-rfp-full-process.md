# RFP Full Process (Request for Proposal — End to End)

## Objectives

Full-process management from requirements definition through RFP issuance, vendor Q&A, and proposal collection, ensuring RFP quality (vendors can understand, respond, and be easily compared).

---

## Prerequisites
- Technology selection/procurement requirements have received internal approval
- Budget range has been determined
- Key evaluation criteria have been agreed upon by all stakeholders
- Decision has been made to use RFP (rather than direct negotiation/single source)

## Inputs
- Business requirements document / technical requirements list
- Procurement strategy (competitive bid / negotiated / single source)
- Vendor long list
- Budget ceiling + timeline

---

## Operation Steps

### Step 1: Build Vendor Long List

#### 1.1 Initial Vendor Screening Sources

| Source | Applicable Scenario |
|------|---------|
| Gartner Magic Quadrant / Forrester Wave | Enterprise software (SaaS/ERP/CRM, etc.) |
| Industry reputation / peer recommendations | Implementation services / professional services |
| Open-source community activity | Open-source technology selection |
| Partner ecosystem | Selecting ecosystem vendors (e.g., SAP/cloud vendor ecosystem) |
| Consulting firm's own experience | Team hands-on experience |

#### 1.2 Narrow Long List to Short List (3-5 vendors)

Screening criteria:
- Functional coverage: Meets >80% of core requirements
- Industry cases: 3+ similar-scale cases in the same industry
- Local support: Has a service team in the client's region
- Financial stability: Won't go bankrupt within 2 years (check funding/public company financials/cash flow)
- Cultural fit: Compatibility with the client's culture/working style

**Screening template:**
| Vendor | Function | Industry Cases | Local Support | Financial | Culture | Screening Result |
|--------|------|---------|---------|------|------|---------|
| A | 85% | 5 cases | Yes (50 people) | Public company | Fit | ✅ Shortlist |
| B | 70% | 1 case | No (overseas) | Series B | Unknown | ❌ Not invited |
| C | 90% | 10 cases | Yes (200 people) | Public company | Fit | ✅ Shortlist |
| D | 88% | 3 cases | Yes (20 people) | Profitable | Fit | ✅ Shortlist |

**Shortlist size**: 3-5 vendors (fewer than 3 = insufficient competition, more than 5 = evaluation cost too high)

---

### Step 2: Draft the RFP Document

#### 2.1 RFP Document Structure

A complete RFP document should include the following chapters:

```
Chapter 1: Project Overview
├── Company introduction: 1-2 paragraphs, what the client does
├── Project background: Why this project is being undertaken
├── Project objectives: What specifically needs to be achieved (quantified)
├── Project scope: What is included, what is not included
└── RFP timeline: Key dates

Chapter 2: Business Requirements
├── Business scenario description (in business language, not technical language)
├── Current pain points (what they are, why they must be resolved now)
└── Expected business outcomes (quantified)

Chapter 3: Technical Requirements (level of detail: better too much than too little)
├── Functional requirements (by priority: Must-have / Should-have / Could-have)
├── Non-functional requirements (performance / security / availability / scalability)
├── Integration requirements (which systems to connect to, what protocols)
├── Data requirements (data volume / format / migration / residency)
├── Technical environment (existing tech stack, constraints)
└── Security and compliance requirements

Chapter 4: Vendor Qualification Requirements
├── Company qualifications (founding date / size / financial status)
├── Industry experience (same-industry cases, including referenceable clients)
├── Implementation capability (team size / methodology / certifications)
├── Support services (SLA / response time / upgrade process)
└── Partner relationships (if applicable)

Chapter 5: Implementation and Project Requirements
├── Expected timeline
├── Implementation methodology requirements
├── Training and knowledge transfer requirements
├── Change management requirements
└── Acceptance criteria (the more specific, the fewer disputes later)

Chapter 6: Commercial Requirements
├── Pricing structure (require pricing by specified dimensions for easy cross-comparison)
├── Payment terms (expected)
├── Key contract clause requirements
└── Intellectual property / data ownership

Chapter 7: Evaluation Process and Criteria
├── Evaluation stages (written → demo → PoC → negotiation)
├── Evaluation dimensions and weights (transparent and public)
├── Proposal format requirements (page count / format / language / deadline)
└── Contact information and Q&A process

Chapter 8: Appendix
├── Glossary
├── Detailed existing technical environment
└── Data samples (anonymized)
```

#### 2.2 Key Considerations

**Functional requirements writing standard:**
```
❌ Poor: "The system should support user management"
✅ Good: "The system needs to support account management for at least 500,000 users, including:
     - User registration (phone + email + third-party accounts)
     - Role and permission management (at least 5 levels of custom roles)
     - User lifecycle management (create → activate → suspend → deactivate)
     - Batch import/export (single batch >100k records, <5 minutes)
     - Login security (support MFA / abnormal login detection / multi-failure lockout)"

Principle: Every requirement must be verifiable — "did the vendor deliver it or not?"
```

**Pricing table standardization (mandatory):**
Attach a standardized pricing template to the RFP — this is key to cross-comparison:

```
Vendor Name: [_________]

I. Software Licenses (Annual/Subscription)
  1.1 Core platform license: [$____] x [____] users = $[____]
  1.2 Add-on modules: [$____] x [____] = $[____]
  ...

II. Implementation Services (One-time)
  2.1 Project management: [____] person-days x $[____] = $[____]
  2.2 Configuration/development: [____] person-days x $[____] = $[____]
  2.3 Testing: [____] person-days x $[____] = $[____]
  2.4 Training: [____] person-days x $[____] = $[____]
  ...

III. Annual Maintenance/Support
  3.1 Standard support (5×8): $[____]/year
  3.2 Premium support (7×24): $[____]/year
  ...

IV. Other Costs (please itemize)
  ...

5-Year Total Cost of Ownership (TCO) Summary:
  Year 1: $[____]
  Year 2: $[____]
  Year 3: $[____]
  Year 4: $[____]
  Year 5: $[____]
  5-Year Total: $[____]
```

---

### Step 3: Develop RFP Timeline

**Standard RFP timeline (typically 8-12 weeks):**

| Phase | Timing | Activity |
|------|------|------|
| RFP Issuance | Week 1 Day 1 | Formal email to shortlisted vendors |
| Vendor Confirmation of Participation | Week 1 Day 3 | Vendors reply whether they will participate |
| Vendor Written Questions Deadline | Week 2 Day 5 | All questions submitted through formal channels |
| Client Releases Q&A (to all vendors) | Week 3 Day 3 | Unified response — all vendors see the same answers |
| Proposal Submission Deadline | Week 5 Day 5 | Strict deadline, late submissions not accepted |
| Phase 1 Evaluation (written) | Week 6-7 | Score using scorecard, select 2-3 for demos |
| Vendor Demos | Week 8 | 2-3 hours per vendor, same agenda |
| Phase 2 Evaluation (demos) | Week 9 | Update scores, select 1-2 for PoC |
| PoC / Trial | Week 10-12 | Time-boxed + scope-limited + clear Go/No-Go criteria |
| Final Evaluation & Negotiation | Week 13+ | Composite scoring, enter contract negotiation |

---

### Step 4: Vendor Q&A Management

#### 4.1 Q&A Principles

```
Rules:
1. All questions submitted through formal channels (email/RFP system); no verbal/WeChat/phone questions accepted
2. All vendors receive identical questions and answers (anonymized and distributed to all)
3. Q&A documents are formal supplements to the RFP, carrying equal weight to the RFP body
4. If omissions/errors are discovered in the RFP, formally correct them via "Clarification/Addendum"
```

#### 4.2 Q&A Document Template

```
RFP Q&A — Batch [X]

The following questions and answers apply to all vendors receiving this RFP.

Q1: [Vendor question verbatim (anonymized)]
A1: [Client response]

Q2: [Vendor question verbatim (anonymized)]
A2: [Client response]

...

Supplement / Clarification:
- Original RFP Chapter X, Section Y, [revision details]
- ...

Release Date: [YYYY-MM-DD]
```

---

### Step 5: Proposal Collection and Compliance Check

#### 5.1 Proposal Receipt Checklist

```
□ Received before the deadline? (Late = reject — this rule cannot be broken)
□ Submitted in the required format? (PDF / binding / quantity)
□ All mandatory sections included? (pricing table / case list / team introduction / ...)
□ Pricing within budget range? (if over, is it significantly over — consider direct elimination)
□ Clear accept / reject / exception clauses? (must flag if core RFP terms are not accepted)
□ Supported by vendor qualifications / case studies?
```

#### 5.2 Handling Non-Compliant Submissions

```
Late submission: Reject outright (unless force majeure with evidence, and fair to all vendors)
Format non-compliance: Allow 24 hours to correct (format only, content cannot change)
Missing key pricing: Require supplement within 24 hours, otherwise excluded from scoring
Non-acceptance of core terms: May enter scoring, but must be reflected in scores (risk deduction)
```

---

## Outputs
1. **Vendor long list → short list screening record**
2. **Complete RFP document** (use templates/RFP Request for Proposal template.md)
3. **Standardized pricing table** (sent to vendors)
4. **Q&A records** (multiple batches)
5. **Proposal receipt and compliance check record**

---

## Quality Checklist
- [ ] Requirements in RFP are verifiable (each requirement can be judged "delivered / not delivered")
- [ ] Pricing table is standardized, ensuring vendor pricing is cross-comparable
- [ ] Evaluation criteria and weights are transparently disclosed in the RFP
- [ ] Q&A is fair and consistent for all vendors
- [ ] Timeline is reasonable, giving vendors sufficient response time (at least 3 weeks)
- [ ] RFP contains no biased language (favoring only one vendor)

---

## Common Pitfalls

| Pitfall | Why It's Wrong | Correct Approach |
|------|---------|---------|
| RFP requirements too vague | Vendor proposals become completely different, impossible to cross-compare, endless disputes later | Spend 60% effort writing clear requirements, 40% on evaluation |
| Inviting too many vendors | 10 responses = evaluation team exhausted, averaging 1 hour per vendor = also unfair | Shortlist 3-5, evaluate each one thoroughly |
| "Close relationship" with one vendor | Leaking information early / tailoring requirements to favor a specific product = unfair, and potentially illegal | All communication through formal channels, all vendors receive identical information |
| Ignoring internal stakeholders | IT picks A, business likes B, boss's friend recommends C — three-way battle | Align internally before RFP, confirm evaluation criteria and weights |
| Not checking vendor references | "10 case studies" → but vendor may have only done a small part | Request 2-3 contactable reference clients, and actually call them |
| Opaque scoring criteria | After bidding ends, rejected vendors ask "why not me?" — inability to explain clearly = risk | Publish scorecard weights in RFP, maintain written records of scoring process |