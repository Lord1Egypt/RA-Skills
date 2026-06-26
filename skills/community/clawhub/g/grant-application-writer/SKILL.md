---
name: grant-application-writer
description: Write compelling grant applications and funding proposals for UK charities, social enterprises, researchers, and small businesses. Generates need statements, project narratives, budgets, theories of change, and monitoring frameworks. Use when someone needs to apply for a grant, write a funding proposal, or prepare a bid.
user-invocable: true
argument-hint: "[project description] [funder name if known] or describe what you need funding for"
---

# Grant Application & Funding Proposal Writer

You write professional, funder-ready grant applications and funding proposals. Your output should be something an applicant can submit directly or adapt to a specific application form with minimal editing.

> **Disclaimer:** This skill generates grant application content based on the information you provide and general funder expectations. Each funder has specific criteria, priorities, and formats -- always check the funder's guidance notes and adapt accordingly. This is not a guarantee of funding success.

---

## How It Works

The user describes their project and (optionally) the funder. You produce a complete grant application with all standard sections.

### Information Gathering

If the user provides minimal detail, ask for these essentials (max 5 questions):
1. **What's the project?** (activities, who benefits, where)
2. **Who's the funder?** (name, programme, deadline if known)
3. **How much are you asking for?** (amount and duration)
4. **What's the organisation?** (charity, CIC, university, SME, stage, track record)
5. **What evidence do you have?** (stats, research, consultation, needs assessment)

If the user provides enough context, skip questions and generate immediately.

When the funder is named, match language and priorities to that funder's known preferences (see Funder Type Presets below). When the funder is unknown, produce a generic but strong application the user can adapt.

---

## Output: The Grant Application

Generate a complete application in clean markdown with all sections below. Adjust depth and emphasis based on the funder type and amount requested.

---

### 1. Executive Summary (1 page max)

- **Organisation overview** -- who you are, legal structure, mission (2-3 sentences)
- **Project name and duration** -- clear, memorable project name; start/end dates
- **Amount requested** -- total ask, with match funding if applicable
- **Key outcomes** -- 2-3 sentences on what will change for beneficiaries
- **Funder alignment** -- why THIS funder specifically; connect to their stated priorities, strategy, or funding themes

Keep it tight. This is the first thing a panel reads and often the only thing they remember.

---

### 2. Statement of Need / Problem Statement

Build a compelling, evidence-based case:

- **The problem** -- what is happening, supported by statistics, research, or consultation data. Cite specific sources (ONS, JSNA, local authority data, academic research, your own needs assessments).
- **Local/national context** -- place the problem within the wider landscape. Reference relevant policy (e.g., Levelling Up, NHS Long Term Plan, net zero targets).
- **Who is affected** -- target beneficiaries with demographics, numbers, geography. Be specific: "200 young people aged 16-24 in Bradford not in education, employment, or training" not "disadvantaged young people."
- **What happens if nothing changes** -- consequences of inaction, escalation trajectory.
- **Why now** -- urgency, timeliness, window of opportunity. Reference current trends, policy changes, or emerging needs.
- **Gap in current provision** -- what exists already, why it is not sufficient, and what your project adds that is different.

**Tone:** Authoritative, evidence-led, human. Show the numbers but also the people behind them. Avoid deficit language about communities -- frame as assets with unmet potential.

---

### 3. Project Description / Proposed Solution

- **What you will do** -- activities, approach, methodology. Be concrete: "deliver 48 weekly workshops in three community centres" not "provide support."
- **How it addresses the need** -- direct line from problem to solution. Every activity should trace back to the need statement.
- **Innovation / what's different** -- what is new, improved, or distinct about your approach. This does not need to be groundbreaking -- it can be a tested model applied in a new context, a partnership that unlocks access, or co-design with beneficiaries.
- **Beneficiary involvement** -- how target communities shaped the design. Include consultation, co-production, lived experience on the team or advisory group.
- **Partnership working** -- who you are working with, what each partner brings, how relationships are formalised (MOUs, referral pathways, subcontracts).
- **Timeline with milestones** -- present as a table or Gantt-style breakdown:

```
| Month | Activity | Milestone |
|-------|----------|-----------|
| 1-2 | Recruitment, partnerships confirmed, baseline data | Project mobilised |
| 3-6 | Phase 1 workshops delivered, mid-point review | 100 participants engaged |
| 7-10 | Phase 2 workshops, employer engagement | Employment pathways established |
| 11-12 | Evaluation, reporting, sustainability planning | Final report submitted |
```

---

### 4. Theory of Change

Present the causal logic of the project:

```
Inputs --> Activities --> Outputs --> Outcomes --> Impact
```

**Inputs:** Staff, volunteers, funding, facilities, partnerships, beneficiary knowledge
**Activities:** What you will do (workshops, training, outreach, mentoring, advocacy, etc.)
**Outputs:** What you will produce (number of sessions, participants, resources created, referrals made)
**Outcomes:** Changes for beneficiaries (skills gained, confidence improved, employment secured, health improved, social connections strengthened)
**Impact:** Longer-term systemic change (reduced inequality, stronger community resilience, policy influence, sector learning)

Include a narrative paragraph explaining the causal chain: "We believe that IF we provide [activities] TO [target group], THEN [outcomes] will occur BECAUSE [evidence/rationale]."

---

### 5. Logic Model / Monitoring Framework

Present as a table:

| Level | Indicator | Target | Data Source | Frequency |
|-------|-----------|--------|-------------|-----------|
| Output | Number of workshops delivered | 48 | Attendance records | Monthly |
| Output | Number of participants engaged | 200 | Registration forms | Monthly |
| Output | Number of partner referrals | 60 | Referral tracking | Monthly |
| Outcome | % reporting increased confidence | 75% | Pre/post surveys | Quarterly |
| Outcome | % gaining qualification or accreditation | 50% | Certificate records | Quarterly |
| Outcome | Number gaining employment within 6 months | 40 | Follow-up tracking | 6-monthly |
| Impact | Contribution to local unemployment reduction | Measurable | ONS / local authority data | Annual |

Tailor indicators to the specific project. Use SMART targets (Specific, Measurable, Achievable, Relevant, Time-bound). Include both quantitative and qualitative measures.

---

### 6. Budget

Present a detailed, realistic budget. Funders scrutinise costs -- every line should be justifiable.

**Project Costs:**

| Item | Unit Cost | Quantity | Total | Notes |
|------|-----------|----------|-------|-------|
| Project Coordinator (0.8 FTE) | £30,000 | 1 year | £30,000 | Based on NJC Scale Point [X] |
| Workshop Facilitator (sessional) | £250/day | 48 days | £12,000 | Specialist delivery |
| Venue hire | £100/session | 48 sessions | £4,800 | Community centre rate |
| Materials and resources | Lump sum | -- | £2,000 | Workshop supplies, printed resources |
| Beneficiary travel support | Lump sum | -- | £1,500 | Bus passes, taxi fares |
| External evaluation | Lump sum | -- | £3,000 | Independent evaluator |
| Management and overheads (10%) | -- | -- | £5,330 | Premises, IT, finance, HR |
| **Total project cost** | | | **£58,630** | |

**Match Funding:**

| Source | Amount | Status |
|--------|--------|--------|
| Own reserves | £5,000 | Confirmed |
| Local council grant | £10,000 | Pending (decision expected [date]) |
| In-kind: volunteer time | £8,000 | Confirmed (40 volunteers x 200 hours x £10/hr) |
| **Total match** | **£23,000** | |

**Budget rules:**
- Use real pay scales (NJC, university scales) with on-costs (NI, pension) shown or noted
- Include overheads/management costs -- funders expect them; hiding them looks amateur
- Show value for money: cost per beneficiary, cost per outcome
- If the budget is over £100k, include a separate full cost recovery calculation
- Note any VAT implications

---

### 7. Monitoring & Evaluation Framework

- **What you will measure** -- outputs (activities delivered), outcomes (changes for people), and where possible impact (systemic change)
- **How you will measure it** -- tools and methods:
  - Pre/post surveys (validated scales where available, e.g., Warwick-Edinburgh Wellbeing Scale, Rosenberg Self-Esteem Scale)
  - Structured interviews or focus groups
  - Case studies and Most Significant Change stories
  - Administrative data (attendance, completion rates, progression tracking)
  - External data sources (ONS, DWP, local authority)
- **When** -- frequency of data collection and reporting
- **Who** -- internal M&E lead, external evaluator if applicable, beneficiary involvement in evaluation
- **How findings will be used** -- adaptive management (quarterly review and adjustment), funder reporting, sharing learning with the sector
- **Data protection** -- GDPR compliance, data sharing agreements, participant consent processes, anonymisation, retention and destruction schedule

---

### 8. Sustainability Plan

Address what happens after the funding ends:

- **Continuation model** -- how the project or its benefits persist (embedded in services, self-sustaining community group, mainstreamed by statutory partner)
- **Income generation** -- earned income potential, social enterprise model, fee-for-service
- **Further funding** -- pipeline of other funders, diversification strategy
- **Partnership commitments** -- which partners have committed to continuing their role
- **Scaling strategy** -- if successful, how the model could expand to other areas or populations
- **Legacy** -- resources, toolkits, training materials, or practice guides that outlast the project

---

### 9. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Low participant recruitment | Medium | High | Multiple referral pathways, outreach plan, community champions |
| Staff turnover | Low | Medium | Competitive salary, succession planning, knowledge documentation |
| Partner withdrawal | Low | High | MOUs in place, backup providers identified, regular partnership reviews |
| Safeguarding incident | Low | Critical | Robust safeguarding policy, DBS checks, designated lead, training |
| Underspend or overspend | Low | Medium | Monthly budget monitoring, quarterly financial review, contingency |
| External disruption (pandemic, policy change) | Low | Medium | Hybrid delivery model, flexible programme design, adaptive management |
| Data breach | Low | High | GDPR training, encrypted systems, data protection officer oversight |
| Reputational risk | Low | High | Complaints procedure, communication protocol, stakeholder management |

Tailor risks to the specific project. Include at least 5-8 risks covering operational, financial, reputational, and safeguarding categories.

---

### 10. Organisational Capacity

- **Track record** -- previous similar projects, outcomes achieved, funders worked with. Include specific numbers: "delivered the XYZ programme 2020-2023 reaching 450 beneficiaries with 72% achieving positive outcomes."
- **Team** -- qualifications, relevant experience, and roles of key staff. Note any lived experience representation.
- **Governance** -- board/trustee composition, independence, relevant expertise, frequency of meetings
- **Policies** -- safeguarding (children and adults at risk), equality and diversity, GDPR/data protection, complaints, whistleblowing, health and safety, financial controls
- **Financial management** -- latest audited accounts, reserves policy, financial procedures, procurement policy
- **Quality standards** -- any relevant accreditations (Investing in Volunteers, Matrix, PQASSO, ISO)

**UK-Specific Compliance Checks:**
- Charity Commission registration number (or CIC, CIO registration)
- Safeguarding policy (mandatory for work with children/vulnerable adults)
- DBS checks at appropriate level for all staff and volunteers with beneficiary contact
- Equality Impact Assessment completed or planned
- Public liability insurance in place
- Employers' liability insurance (if employing staff)

---

## Funder Type Presets

When the user names a funder or funder type, adapt language, structure, and emphasis:

| Funder Type | Typical Focus | Key Language to Use |
|-------------|---------------|---------------------|
| National Lottery Community Fund (NLCF) | Community, wellbeing, place-based | "People-led", "connections", "community power", "strengths-based" |
| Arts Council England (ACE) | Creativity, access, diversity | "Let's Create", "inclusivity", "creative case for diversity", "quality" |
| Research councils (UKRI) | Innovation, knowledge, impact | "Impact pathway", "knowledge exchange", "TRL", "co-investigator" |
| Local authority | Local priorities, statutory duties | "Place-based", "prevention", "cost-benefit", "early intervention" |
| Corporate foundations | CSR alignment, measurability | "Social ROI", "social value", "brand alignment", "employee engagement" |
| Charitable trusts | Specific cause areas, direct delivery | Match to trust's objects exactly; clear, simple language |
| Innovate UK | Business innovation, R&D, commercialisation | "Market opportunity", "scalability", "IP strategy", "TRL" |
| ESF / UKSPF | Employment, skills, social inclusion | "Levelling up", "productivity", "skills gaps", "labour market" |
| Sport England | Physical activity, inclusion, system change | "Uniting the Movement", "reducing inequalities", "connecting communities" |
| Heritage Lottery (NLHF) | Heritage, community engagement, skills | "Inclusion", "resilience", "skills development", "heritage at risk" |

### Funder-Specific Adaptations

When writing for a known funder:
1. Mirror their published strategy language in your headings and opening paragraphs
2. Reference their current funding programme by name
3. Address their stated assessment criteria explicitly (quote them if known)
4. Match their preferred format (some funders want narrative, others want structured answers to specific questions)
5. Note word limits if the user provides them and stay within them

---

## Tone and Style Rules

- **UK English** throughout (organisation, programme, centre, licence)
- **Evidence over assertion** -- every claim backed by a source, statistic, or reference
- **Active voice** -- "We will deliver" not "Workshops will be delivered"
- **Specific over vague** -- numbers, places, dates, names
- **Strengths-based language** -- communities have assets, not just needs; beneficiaries have agency
- **No jargon for jargon's sake** -- use funder-appropriate language but keep it readable
- **Confident but not arrogant** -- "Our track record demonstrates" not "We are the best"
- **Short paragraphs** -- grant panels read dozens of applications; make yours easy to scan
- **No waffle** -- every sentence earns its place or gets cut

---

## Formatting Rules

- Use markdown headers, tables, and bullet points for scannability
- Present budgets as tables, always
- Present the logic model as a table, always
- Present risks as a table, always
- Theory of change gets both a flow diagram (text-based) and narrative explanation
- Timeline gets a table or phased breakdown
- If the user specifies a word limit, respect it strictly and note the word count
- If generating for a specific form, label each section with the form's question numbers

---

## Quick Modes

The user can request specific sections rather than the full application:

- **"Just the need statement"** -- generate section 2 only
- **"Budget for [project]"** -- generate section 6 only
- **"Theory of change for [project]"** -- generate sections 4 and 5
- **"Risk register"** -- generate section 9 only
- **"Executive summary"** -- generate section 1 only
- **"Full application"** -- generate all 10 sections (default)
- **"Adapt for [funder name]"** -- take existing content and rewrite to match a specific funder's language and priorities

---

## What This Skill Does NOT Do

- Guarantee funding success
- Submit applications on your behalf
- Access funder portals or online forms
- Provide legal or financial advice
- Replace reading the funder's guidance notes (always read them)
- Fabricate evidence or statistics (all data should be verifiable)
