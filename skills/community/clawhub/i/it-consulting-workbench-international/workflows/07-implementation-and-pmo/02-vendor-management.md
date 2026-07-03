# Vendor Management

## Objectives

Manage vendor relationships from contract signing through project delivery to long-term operations, ensuring vendors deliver as committed, and building healthy, performance-driven vendor relationships.

---

## Prerequisites
- Vendor contract / SOW has been signed
- Vendor team has been confirmed
- Internal vendor management owner has been designated

## Inputs
- Signed contract / SOW / SLA
- Vendor team roster and roles
- Project plan (including vendor deliverables and milestones)
- Reward and penalty clauses in the contract

---

## Operation Steps

### Step 1: Establishing the Vendor Relationship

#### 1.1 Vendor Classification Management

Not all vendors are managed the same way:

| Vendor Type | Characteristics | Management Intensity | Management Focus |
|-------------|----------------|----------------------|------------------|
| **Strategic Partner** | Long-term / large value / core system dependency | High | Executive relationship + joint planning + innovation collaboration |
| **Project Delivery Partner** | Single project / fixed scope / fixed timeline | Medium-High | Delivery management + quality control + contract compliance |
| **Service Provider** | Operations / Support / Cloud services / ongoing services | Medium | SLA monitoring + service reviews + renewal management |
| **Commodity Vendor** | Hardware / Licenses / standardized products | Low | Price + delivery + compliance |

#### 1.2 Vendor Kickoff

Five things that must be done after signing and before formal work begins:

```
1. Vendor Kickoff Meeting
   - Align on project goals (not just contract scope, but "why we are doing this")
   - Confirm communication channels and escalation paths (both sides)
   - Confirm key milestones and timeline
   - Most importantly: Build mutual trust and a collaborative relationship, not "client vs vendor"

2. Unified Ways of Working and Tools
   - Which project management tool? (Jira/Trello/...)
   - Where is the code repository? How are permissions set?
   - What for document collaboration? (Confluence/Notion/...)
   - What for communication? (Slack/Teams/WeChat?)

3. Personnel Confirmation
   - Are the key personnel named in the contract actually in place now?
   - Are each person's role and responsibilities clear?
   - Who are the backup personnel?

4. Delivery Standard Alignment
   - What counts as "Done"? (Definition of Done)
   - What format for documentation? How detailed?
   - How to judge acceptance criteria (objective, testable)?

5. First Joint Risk Review
   - Each side raises their Top 3 concerns about the project
   - Discuss how to address them together
```

---

### Step 2: Vendor Performance Management

#### 2.1 Vendor Scorecard (Quarterly)

| Dimension | Weight | Q1 | Q2 | Q3 | Q4 | Notes |
|-----------|--------|----|----|----|----|-------|
| Delivery Quality | 25% | [1-5] | [1-5] | [1-5] | [1-5] | Defect rate / rework rate / acceptance pass rate |
| Delivery Timeliness | 25% | [1-5] | [1-5] | [1-5] | [1-5] | % milestones/tasks completed on time |
| Cost Control | 15% | [1-5] | [1-5] | [1-5] | [1-5] | Budget variance / change cost reasonableness |
| Responsiveness & Communication | 15% | [1-5] | [1-5] | [1-5] | [1-5] | Issue response speed / communication quality |
| Team Stability | 10% | [1-5] | [1-5] | [1-5] | [1-5] | Key personnel changes / knowledge continuity |
| Innovation / Value-Add | 10% | [1-5] | [1-5] | [1-5] | [1-5] | Proactive improvement suggestions / industry insights shared |
| **Weighted Total** | | | | | | |

Scoring Criteria:
- 5: Exceeds expectations — not only delivers well within contract, but also provides additional value
- 4: Meets expectations — delivers per contract, no issues
- 3: Basically meets — overall OK but with some minor issues
- 2: Unsatisfactory — recurring problems, requires management escalation
- 1: Severely unsatisfactory — consider replacement / contract termination

#### 2.2 Quarterly Business Review (QBR)

**Agenda (90 minutes):**
```
0:00-0:15  Review past quarter (QoQ): Scorecard + key events + achievements
0:15-0:30  Client-side feedback: What went well / what needs improvement (specific + with examples)
0:30-0:45  Vendor-side feedback: Challenges they face / areas where the client needs to improve
0:45-1:00  Market / Technology trends: Share industry developments + new products/capabilities
1:00-1:20  Next quarter outlook: Plans + risks + opportunities
1:20-1:30  Action item confirmation

Required attendee seniority:
- Client side: At least IT Director level + Procurement representative
- Vendor side: At least Client Director / VP level
```

---

### Step 3: Contract & SLA Management

#### 3.1 SLA Monitoring Dashboard

| SLA Metric | Commitment | Actual (YTD) | Met? | Trend |
|------------|-----------|--------------|------|-------|
| System Availability | 99.9% | 99.95% | ✅ | → |
| P1 Response Time | <15 min | 8 min | ✅ | ↓ (faster) |
| P1 Resolution Time | <4 hours | 3.2 hours | ✅ | → |
| P2 Response Time | <1 hour | 2.5 hours | ❌ | ↑ (deteriorating) |
| Change Success Rate | >99% | 98.5% | ❌ | ↓ |

#### 3.2 SLA Breach Handling

```
SLA breach occurs →
├── First occurrence: Require vendor to provide Root Cause Analysis (RCA) within 24 hours
├── Monthly breaches >3: Formal Corrective Action Plan (CAP) — vendor produces, client reviews
├── Quarterly severe breach (e.g. availability <99.5%): Trigger Service Credit +
│   Vendor executive explains in person
└── Persistent breaches with ineffective CAP: Trigger "exit clause" evaluation in the contract
```

**Service Credits are not the goal**: Penalizing vendors is not the objective; service restoration is. If a vendor would rather pay penalties than improve service, it's time to switch.

#### 3.3 Contract Change Management

When the contract / SOW needs to be modified:

```
1. Document the change request: What is changing / Why / Impact (schedule/cost/quality) / Alternatives
2. Internal approval: PM → Core Team → Sponsor (tiered by amount)
3. Negotiate with vendor: Fair pricing (benchmarked) + reasonable timeline
4. Sign the change order: A formal document, not just an email confirmation
5. Update all related documents: Project plan / Budget / Scope statement / Risk register
```

---

### Step 4: Vendor Risk & Relationship Management

#### 4.1 Vendor Risk Signals

When the following signals appear, immediate attention is required:

| Signal | May Indicate |
|--------|-------------|
| Frequent key personnel changes | Internal problems / project is not being prioritized |
| Slowing responsiveness | Taking on larger clients / team is under-resourced |
| Starting to haggle over small things | This project is not profitable for them / they want to exit |
| Sudden quality drop | Core team has been pulled to other projects |
| Communication becoming opaque | Something is being hidden |
| Frequent change requests (asking for more money) | Low-balled the bid initially / different understanding of scope |

**Response:**
- Don't wait until problems accumulate and explode before addressing them
- At the first signal, proactively schedule a conversation with vendor leadership: "We've noticed XXX — is there something we need to solve together?"
- A good vendor relationship = able to communicate candidly, not "client audits vendor"

#### 4.2 Vendor Exit Management

When a vendor needs to be replaced:

```
Transition Checklist:
□ Are all code / documents / configurations in the client's possession (not the vendor's)?
□ Have all system admin passwords / API keys / certificates been handed over?
□ Has data been fully exported and verified?
□ Is there vendor-specific knowledge that needs to be extracted and documented?
□ Are there ongoing tasks / unresolved bugs that need handover?
□ Are there contractual constraints (e.g. must give 90 days' notice)?
□ Is the new vendor in place and has knowledge transfer been completed?
□ Have key interfaces / dependencies been identified with transition plans?
□ Have business stakeholders been informed of potential impacts during the transition?

Vendor transition period = the most vulnerable period
- The outgoing vendor may no longer care ("we're not renewing anyway")
- The incoming vendor may not yet be familiar
- Recommendation: Run old and new vendors in parallel for at least 1 month
```

---

### Step 5: Vendor Relationship Health

#### 5.1 Characteristics of a Healthy Vendor Relationship

```
✅ Both sides have balanced investment and benefit (not one side "bleeding" the other)
✅ Issues can be discussed candidly — no "the vendor always says yes yes yes"
✅ Vendor proactively proposes improvements, not just passively executing
✅ Both sides have willingness for long-term collaboration (but that doesn't mean no performance review)
✅ Key personnel on both sides know each other and have trust
✅ The contract is a "guide" not a "weapon" (but can be used when necessary)
```

#### 5.2 Behaviors That Destroy Vendor Relationships

```
❌ Unjustified payment delays (vendors will "compensate" by reducing service quality)
❌ Belittling the vendor team in front of them (a partnership is not a master-servant relationship)
❌ Frequent requirement changes without additional time or money (vendors will recoup on quality)
❌ Escalating minor issues all the way to the CEO (a bug does not need CEO-level discussion)
❌ Constantly threatening "we'll find someone else" (if you really can, just do it; if you can't, threats only poison the relationship)
❌ Not managing the vendor relationship properly; slashing prices to the point of loss (nobody does good work on a loss-making deal)
```

---

## Outputs
1. **Vendor Classification & Management Strategy**
2. **Vendor Kickoff Record** (incl. ways of working / tools / personnel / delivery standards)
3. **Vendor Scorecard** (updated quarterly)
4. **QBR Meeting Minutes** (quarterly)
5. **SLA Monitoring Dashboard** (updated monthly)
6. **Vendor Risk Signal Checklist & Responses**
7. **Vendor Exit / Transition Plan** (if applicable)

---

## Quality Checklist
- [ ] Each key vendor has a clearly designated internal management owner
- [ ] SLA metrics are measurable (not "as soon as possible")
- [ ] QBR is not a formality — substantive conversation, senior-level attendance from both sides
- [ ] Vendor scorecard is backed by objective data, not subjective feeling
- [ ] All contract changes have written records
- [ ] Vendor exit planning begins at contract signing (yes, think about how to exit from the very beginning)

---

## Common Pitfalls

| Pitfall | Why It's Wrong | Correct Approach |
|---------|---------------|------------------|
| Only looking at the contract, ignoring the relationship | Constantly waving the contract: "Clause 3.2 says you must..." — the relationship is destroyed, and with it, collaborative flexibility | Contract = baseline protection; Relationship = day-to-day collaboration. Both are needed. |
| Not investing in the vendor relationship | Assuming that once the contract is signed, the vendor should just perform well | Regular communication / clear expectations / give feedback / recognize good performance — manage key vendors like you manage your team |
| Trusting the vendor completely | "They're the professionals, we don't need to manage them" — then discover 3 months later they've gone off track | Trust but Verify: independent reviews + regular check-ins |
| Undifferentiated management | Using the same management process for a $500 office supplies vendor and a $5M systems vendor | Tiered management: invest in relationships with strategic vendors; commodity vendors only need basic compliance checks |
| Slow payment | Vendor cash flow is strangled → service quality drops → client dissatisfaction → vicious cycle | Pay on time (there's an internal metric called "on-time payment rate" in vendor evaluations) |
| Leaving knowledge with the vendor | The vendor leaves, and you know nothing | Knowledge transfer is a mandatory clause in the contract and must be continuously executed during the project |