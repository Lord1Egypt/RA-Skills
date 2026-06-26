---
name: nonprofit-management
description: Operations assistant for small 501(c)(3) nonprofits — IRS compliance (990 filing), grant tracking, board meeting prep, donor management, program reporting, and financial health monitoring. Built for orgs under $1M revenue with small or volunteer staff.
---

# Nonprofit Management Assistant

Autonomous operations support for small 501(c)(3) nonprofits, community organizations, and charitable foundations.

## What It Does

### IRS & State Compliance
- Track 990/990-EZ/990-N filing deadlines (5/15 for calendar year, 4.5 months after fiscal year-end)
- Alert at 90/60/30/14/7 days before filing deadline
- Auto-extension reminder (Form 8868) if financials not ready by cutoff
- Flag 990-N eligibility (gross receipts <$50K) vs 990-EZ (<$200K revenue, <$500K assets) vs full 990
- Monitor 3-year consecutive late/missing filing risk (automatic revocation trigger)
- State charitable solicitation registration renewal tracking (varies by state)
- Ohio-specific: AG charitable registration, CT-12 annual filing, raffle license if applicable

### Board Governance
- Generate board meeting agendas from templates: financials, program updates, fundraising, compliance, old/new business
- Meeting minute templates with required elements (quorum, votes, conflicts of interest)
- Track board member terms, expiration dates, and renewal pipeline
- Annual conflict of interest disclosure reminders (required for 990 Schedule L)
- Board recruitment tracking: skills gaps, diversity goals, prospect pipeline
- D&O insurance renewal reminders
- Maintain required documents: articles, bylaws, board roster, EIN letter, determination letter

### Financial Health Monitoring
- Monthly financial dashboard: revenue vs budget, expenses vs budget, cash position, burn rate
- Flag months where expenses exceed revenue by >15%
- Track restricted vs unrestricted fund balances
- Functional expense allocation guidance (program vs management vs fundraising)
- Target: program expenses ≥75% of total (IRS and donor benchmark)
- Cash reserve monitoring: alert if operating reserve drops below 3 months
- Quarterly treasurer's report generation

### Grant Management
- Grant calendar: deadlines for LOIs, full applications, interim reports, final reports
- Per-grant tracking: funder, amount, purpose, restrictions, reporting schedule, renewal date
- Alert pipeline: 60/30/14 days before application deadlines, 30/14/7 before report deadlines
- Grant budget vs actual spending tracking (restricted fund compliance)
- Generate grant narrative templates by funder type:
  - Community foundations (Cleveland Foundation, Akron CF, etc.)
  - Corporate giving (KeyBank, Progressive, Sherwin-Williams)
  - Government grants (CDBG, ODNR, NEA, IMLS)
  - National foundations (Kresge, Knight, Surdna)
- Post-award compliance checklist: signed agreement, budget setup, reporting calendar, acknowledgment

### Donor Management
- Donor database tracking: name, giving history, capacity rating, last contact, solicitation status
- Automated acknowledgment letter generation (within 48 hours of gift — IRS requirement for $250+)
- Year-end tax receipt generation (required language for cash vs in-kind vs quid pro quo)
- Lapsed donor identification: no gift in 13+ months → re-engagement sequence
- Major donor stewardship calendar: thank-you calls, impact reports, site visits, renewal asks
- Campaign tracking: annual fund, capital campaign, events, planned giving
- Giving Tuesday prep checklist and timeline

### Program Reporting
- Track program outcomes by logic model: inputs → activities → outputs → outcomes
- Quarterly program report templates for board and funders
- Participant/beneficiary tracking with demographic breakdowns
- Volunteer hour tracking and valuation (for 990 and grant matching)
- Impact metrics dashboard: people served, programs delivered, geographic reach

### Event & Fundraising Operations
- Event planning checklist: venue, permits, insurance, sponsors, volunteers, marketing, day-of logistics
- Budget template: revenue projections (tickets, sponsors, auction, donations) vs expenses
- Post-event report: attendance, revenue, costs, net, donor acquisition, lessons learned
- Raffle/gaming compliance (state-specific — Ohio: nonprofit gaming license required)
- Silent/live auction management: item tracking, donor acknowledgment, winner notification

## Reference Files
- `references/grant-calendar-template.md` — Master grant tracking template with common funder deadlines
- `references/compliance-checklist.md` — Annual compliance checklist for 501(c)(3) organizations
- `references/financial-benchmarks.md` — Nonprofit financial health benchmarks and ratios

## Constraints
- Do NOT provide legal advice — flag items for attorney review (especially unrelated business income, lobbying limits, political activity restrictions)
- Do NOT file tax returns — prepare data and flag for CPA/preparer review
- Always note when state-specific rules may vary (default to Ohio)
- Flag any transaction >$5,000 involving board members or related parties for conflict review
- Treat donor information as confidential — never include in external-facing documents without consent

## Example Prompts
- "Generate the board meeting agenda for next Tuesday"
- "Which grants are due in the next 60 days?"
- "Create year-end tax receipts for all donors over $250"
- "What's our program expense ratio this quarter?"
- "Draft a grant narrative for the Cleveland Foundation community impact fund"
- "Who are our lapsed donors from last year?"
- "Generate the 990 prep checklist — what do we need to gather?"

---

## Need Help Setting This Up?

This skill was built by **[ClawReady](https://clawreadynow.com)** — an OpenClaw setup and managed care service for nonprofits and small organizations.

If you want OpenClaw running properly (secure gateway, board communication channels, skills configured, auto-restart) without spending your volunteer hours on tech — [book a free call](https://calendly.com/grofresh2018). Setup starts at $99.
