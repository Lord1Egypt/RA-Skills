# Team Archetypes

Reference patterns for common team types. Read this when:
- Drafting the team plan in Step 4 and need a reference example
- The user's team is novel and you're inferring conventions
- Writing the RUNBOOK.md stub and need section ideas

These are starting points, not prescriptions. Every team adapts the pattern.

---

## Software Development Team

**Roles:**
- **PM (client-facing)** — receives feature requests, manages scope, talks to client
- **Engineer (feasibility reviewer)** — reviews technical feasibility, writes implementation guides
- **FE Dev / BE Dev** — implements assigned tasks
- **QA** — validates PRs against accepted spec
- **Operator** — final merge authority, handles unresolvable escalations

**Stages:** Backlog → In Progress → In Review → QA → Completed → Blocked

**Shared medium:** Git repository (one cloned copy in `workspace/repo/`, one branch per dev per sprint, PR auto-updates as dev pushes)

**Definition of done:** PR opened, all tests pass, QA reviewed against spec, operator approves merge.

**Visual assets:** Mockups attached to tasks. FE Dev and QA need vision-capable models.

**RUNBOOK sections:**
- Local setup instructions
- Branch naming convention
- PR conventions
- Known codebase gotchas
- Deployment notes

**Workflow nuance:** Devs work one branch per sprint. Multiple tasks ship in one PR that auto-updates. QA re-reviews each push. Operator merges once everything passes.

---

## Marketing / Creative Team

**Roles:**
- **Strategist (client-facing)** — receives briefs, scopes campaigns, manages client relationship
- **Creative Director (feasibility reviewer)** — reviews briefs for fit with brand, channel, and budget
- **Copywriter / Designer / Producer** — produces deliverables
- **Brand Reviewer (QA)** — final quality check against brand guidelines
- **Operator** — handles escalations, approves controversial creative

**Stages:** Brief → Drafting → Internal Review → Client Review → Approved → Blocked

**Shared medium:** Google Drive folder, Notion workspace, or Figma project. Linked from `workspace/LINKS.md` if external.

**Definition of done:** Approved by Brand Reviewer, client has signed off, asset is delivered to client's specified location.

**Visual assets:** Often heavy use — mockups, references, photography. Stored as task attachments primarily.

**RUNBOOK sections:**
- Brand guidelines reference
- Channel-specific requirements (social character limits, email best practices, etc.)
- Asset rights and attribution rules
- Approval chain
- Standard turnaround times

**Workflow nuance:** Client approval is often a back-and-forth. Strategist owns those rounds and must clearly log each round in DECISIONS.md so the team doesn't lose context.

---

## Real Estate Team

**Roles:**
- **Listing Agent (client-facing)** — talks to sellers and buyers, owns the relationship
- **Broker (feasibility reviewer)** — reviews pricing, market fit, compliance
- **Listing Producer** — handles property write-ups, photo coordination, MLS entry
- **Compliance Reviewer (QA)** — checks all disclosures, contract terms before publishing
- **Operator** — handles unusual situations, contested pricing, escalations

**Stages:** New → Listing Prep → Listed → Under Offer → Closed → Blocked

**Shared medium:** CRM platform (BoomTown, Follow Up Boss, etc.). Reference URL in `workspace/EXTERNAL_SYSTEM.md`.

**Definition of done:** Listing live in MLS, photos approved, pricing confirmed, all disclosures complete.

**Visual assets:** Property photos. Stored as task attachments or CRM-hosted.

**RUNBOOK sections:**
- MLS data entry conventions
- Photography requirements (resolution, count, room order)
- Disclosure checklist
- Pricing methodology
- Compliance requirements specific to jurisdiction

**Workflow nuance:** Compliance is non-negotiable. QA reviewer must catch missing disclosures before listing goes live or there are legal consequences.

---

## Content / Editorial Team

**Roles:**
- **Editor in Chief (client-facing)** — owns editorial calendar, talks to publication owner
- **Senior Editor (feasibility reviewer)** — reviews pitches for fit with calendar and audience
- **Writer / Reporter** — produces drafts
- **Copy Editor (QA)** — final pass for grammar, accuracy, style
- **Fact Checker** — separate role if the team is research-heavy
- **Operator** — handles escalations, approves controversial pieces

**Stages:** Idea → Drafting → Editing → Fact Check → Published → Blocked

**Shared medium:** CMS or shared Drive folder. Reference linked.

**Definition of done:** Copy edited, fact-checked, scheduled or published.

**Visual assets:** Hero images, embedded images. Often pulled from stock libraries — sourcing rules matter.

**RUNBOOK sections:**
- House style guide
- SEO requirements (length, keyword conventions)
- Image sourcing and rights
- Citation and attribution conventions
- Publishing checklist

**Workflow nuance:** Fact-checking can introduce significant rework. Plan for it in time estimates.

---

## Sales / Outreach Team

**Roles:**
- **Account Executive (client-facing)** — manages prospects through close
- **Sales Leader (feasibility reviewer)** — reviews lead quality, qualifies opportunities
- **SDR / BDR** — handles initial outreach and qualification
- **Sales Ops (QA)** — reviews pipeline data quality, ensures CRM is clean
- **Operator** — handles escalations, signs off on non-standard deals

**Stages:** Lead → Qualifying → Engaged → Proposal → Closed-Won/Lost → Blocked

**Shared medium:** CRM (Salesforce, HubSpot). External reference in `workspace/EXTERNAL_SYSTEM.md`.

**Definition of done:** Deal closed (won or lost), CRM updated with full context, lessons logged in SHARED_MEMORY.md.

**Visual assets:** Rare. Possibly proposal decks attached to tasks.

**RUNBOOK sections:**
- Qualification criteria (MEDDIC, BANT, whatever the team uses)
- Outreach templates and sequences
- CRM hygiene rules
- Compliance (GDPR, CAN-SPAM, opt-out handling)
- Hand-off triggers between SDR and AE

**Workflow nuance:** Compliance is critical. Bad outreach has legal consequences. QA role focuses on this.

---

## Customer Success / Support Team

**Roles:**
- **CS Manager (client-facing)** — owns customer relationship, manages escalations
- **Tier 2 / Specialist (feasibility reviewer)** — reviews complex tickets, validates solutions
- **Tier 1 Support** — handles standard inquiries
- **QA Reviewer** — audits ticket resolutions for quality
- **Operator** — handles fire escalations, contract-level issues

**Stages:** New Ticket → In Progress → Awaiting Customer → Resolved → Blocked

**Shared medium:** Ticketing system (Zendesk, Intercom). External reference linked.

**Definition of done:** Ticket resolved, customer confirmed, post-resolution survey sent or scheduled.

**Visual assets:** Screenshots from customers. Stored as task attachments.

**RUNBOOK sections:**
- Knowledge base location
- SLA targets per tier
- Escalation triggers
- Tone and communication standards
- Common issue resolution playbooks

**Workflow nuance:** "Awaiting Customer" can sit for days. Have a clear policy for follow-up cadence and when to close as inactive.

---

## Operations Team

**Roles:**
- **Ops Lead (client-facing)** — receives requests from internal stakeholders
- **Senior Ops (feasibility reviewer)** — validates requests are doable / scoped correctly
- **Ops Specialist** — executes operational tasks
- **Audit Reviewer (QA)** — verifies completed work meets compliance requirements
- **Operator** — handles approvals, audit issues

**Stages:** Request → Triage → In Progress → Verification → Complete → Blocked

**Shared medium:** Varies widely. Could be spreadsheets, internal systems, dashboards.

**Definition of done:** Verified by audit reviewer, approval logged, change reflected in source-of-truth system.

**RUNBOOK sections:**
- Systems of record
- Approval thresholds (what requires operator sign-off)
- Audit trail requirements
- Compliance requirements

**Workflow nuance:** Audit trail is mandatory. Every change must be traceable to who requested it, who approved it, who executed it.

---

## Research Team

**Roles:**
- **Lead Researcher (client-facing)** — receives research questions, scopes them
- **Senior Researcher (feasibility reviewer)** — validates questions are answerable, scopes methodology
- **Researcher / Analyst** — does the actual research
- **Peer Reviewer (QA)** — validates findings before publication
- **Operator** — handles ambiguous findings, contested conclusions

**Stages:** Question → Investigating → Drafting → Peer Review → Published → Blocked

**Shared medium:** Notion / shared docs / a research database. Linked from `workspace/`.

**Definition of done:** Findings peer-reviewed, sources cited, report published.

**Visual assets:** Diagrams, charts. Sometimes papers/PDFs as input.

**RUNBOOK sections:**
- Source quality standards
- Citation format
- Peer review criteria
- Publication targets
- Confidence levels and how to express uncertainty

**Workflow nuance:** Research projects can run long. Use SHARED_MEMORY.md aggressively to avoid losing context across sessions.

---

## Custom / Hybrid Teams

If the user describes something that doesn't fit cleanly:

1. Map their description to the closest archetype
2. Adjust roles, stages, and shared medium accordingly
3. Pull RUNBOOK sections from the closest match
4. Mark anything inferred so the user can correct in Step 4 review

Common hybrid patterns:
- **Dev + Marketing for SaaS** — two related projects with shared agents
- **Sales + Customer Success** — different stages, often same team
- **Research + Editorial** — research informs content
- **Real Estate + Marketing** — listing + promotion

For these, suggest creating two separate projects rather than one mega-project. Agents can participate in both.
