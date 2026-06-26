---
name: proposal-kit
description: >
  One-click business proposal package generator. Takes a brief project/service description and
  generates a COMPLETE ready-to-send package: proposal (.docx), pitch deck (.pptx), pricing
  sheet (.xlsx), and executive one-pager (.pdf) — all cohesive and client-ready. Trigger whenever
  the user mentions proposals, quotes, bids, pitch decks, project scopes, SOWs, RFP responses,
  cost estimates, or anything like "send something professional to a client/investor/partner",
  "help me win this deal", "I need to pitch", "quote for a project", "client deliverable",
  or describes any service/product to sell. Works across ALL industries — tech, construction,
  marketing, design, consulting, legal, events, real estate, manufacturing, healthcare, and more.
---

# Proposal Kit — One-Click Business Proposal Generator

## What This Skill Does

Transforms a brief natural language description into a complete, professional proposal package
consisting of 4 coordinated deliverables:

1. **Proposal Document** (.docx) — Full narrative proposal with executive summary, problem statement, proposed solution, methodology, timeline, team, and terms
2. **Pitch Deck** (.pptx) — Visual presentation version for meetings and screen-sharing
3. **Pricing Sheet** (.xlsx) — Itemized cost breakdown with phases, line items, totals, and optional discount tiers
4. **Executive One-Pager** (.pdf) — Single-page summary for decision-makers who won't read the full proposal

All four documents share consistent messaging, tone, and structure — they look like they came from the same professional team.

## Why This Matters

A proposal is the bridge between "interested" and "sold." Most freelancers, agencies, and small businesses lose deals not because their work is bad, but because their proposals look amateur, take too long to produce, or arrive too late. This skill collapses a 4-20 hour process into minutes.

## Workflow

### Step 1: Gather the Brief

Extract the following from the user's message. If critical information is missing, ask — but infer sensible defaults for anything non-critical. The goal is to minimize friction. Real users are busy and impatient; they want results fast.

**Required (ask if missing):**
- What is the project/service? (even a one-sentence description is enough)
- Who is the client? (name/company, or "unnamed client" as default)

**Optional (infer smart defaults):**
- Budget range or pricing approach
- Timeline / delivery schedule
- Industry context
- Specific deliverables or phases
- Team size and roles
- Company name of the proposer (default: use the user's name if known)
- Tone: formal, friendly-professional, or bold (default: friendly-professional)
- Currency (default: USD, but localize based on context clues — if the user writes in Chinese use CNY, Japanese use JPY, etc.)

### Step 2: Build the Content Architecture

Before generating any files, create a unified content plan. This is critical — all 4 documents must tell the same story from different angles.

**Content plan structure:**
```
Project Title: [compelling, specific title]
Tagline: [one sentence that captures the value proposition]
Client Pain Points: [2-3 specific problems this solves]
Proposed Solution: [clear description of what will be delivered]
Key Differentiators: [why choose this team/approach]
Phases: [3-5 project phases with deliverables and timelines]
Pricing: [itemized by phase, with subtotals and total]
Timeline: [start to finish with milestones]
Terms: [payment terms, revision policy, IP ownership basics]
```

### Step 3: Generate All Four Documents

Read the relevant skill files before creating each document type:

- Before creating the .docx: Read `/mnt/skills/public/docx/SKILL.md`
- Before creating the .pptx: Read `/mnt/skills/public/pptx/SKILL.md`
- Before creating the .xlsx: Read `/mnt/skills/public/xlsx/SKILL.md`
- Before creating the .pdf: Read `/mnt/skills/public/pdf/SKILL.md`

#### A. Proposal Document (.docx)

Structure: Cover Page, Table of Contents, Executive Summary, Understanding Your Needs, Proposed Solution, Methodology & Process, Timeline & Milestones, Investment, Why Us, Next Steps, Appendix.

Writing principles:
- Open with the client's world, not yours
- Use "you/your" more than "we/our" — ratio at least 2:1
- Be specific: "reduce onboarding time from 3 weeks to 4 days" beats "improve efficiency"
- Keep it scannable — busy executives read proposals in 3 minutes

Formatting: Professional layout, navy blue #1B365D accent, tables for pricing and timeline, page numbers in footer.

#### B. Pitch Deck (.pptx)

10 slides: Title, The Challenge, Our Approach, Solution Details (3 slides), Timeline, Investment, Why Us, Next Steps.

Design: One idea per slide, minimal text, consistent color scheme matching the docx.

#### C. Pricing Sheet (.xlsx)

Sheet 1 — Pricing Summary: Phase | Description | Deliverables | Timeline | Cost, subtotals, grand total, payment schedule.
Sheet 2 — Detailed Breakdown (optional): line-item detail, hours x rate.
Sheet 3 — Comparison (optional): Basic | Standard | Premium tiers.

Use formulas for all totals. Professional formatting with alternating row colors.

#### D. Executive One-Pager (.pdf)

Single page: Project Title, Tagline, The Challenge, Our Solution, Key Deliverables, Timeline, Investment, Contact.

Design: High information density, clear visual hierarchy, same color scheme, readable in 30 seconds.

### Step 4: Present the Package

Save all files to `/mnt/user-data/outputs/` with naming:
- [Client-Name]-Proposal.docx
- [Client-Name]-Pitch-Deck.pptx
- [Client-Name]-Pricing.xlsx
- [Client-Name]-Summary.pdf

Use `present_files` to deliver all four. Close with: "Here's your complete proposal package for [Client] — 4 documents, all ready to send. Want me to adjust the pricing, tone, or any specific section?"

## Adaptation Guidelines

**For different industries:**
- Construction/Engineering: safety, compliance, certifications, material specifications
- Technology: technical architecture, scalability, security, integration
- Creative/Marketing: creative vision, brand alignment, portfolio references
- Consulting: methodology, frameworks, past results, ROI projections
- Events: logistics, vendor coordination, contingency planning
- Legal: formal tone, precise scope definitions, liability considerations

**For different deal sizes:**
- Under $5K: lean package, shorter proposal
- $5K-$50K: standard package, all 4 documents
- $50K+: add risk mitigation section and case study appendix

**For different languages:**
- Detect the user's language and generate ALL documents in that language
- Adapt cultural norms, formality levels, and document conventions
- Use locally appropriate business formats and currency

## Quality Checklist

Before delivering, verify:
- [ ] All 4 documents tell the same story consistently
- [ ] Pricing matches across all documents
- [ ] Timeline is consistent everywhere
- [ ] Client name is spelled correctly throughout
- [ ] No placeholder text left behind
- [ ] Tone matches the industry and relationship
- [ ] Call to action is clear and specific
- [ ] Documents are properly formatted and professional
