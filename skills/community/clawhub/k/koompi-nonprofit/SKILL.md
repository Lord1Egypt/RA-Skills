---
name: nonprofit
description: Use for nonprofit and NGO operations — donor management, grant tracking, fundraising campaigns, volunteer coordination, program impact measurement, board governance, event planning, fund accounting, compliance reporting, and stakeholder communications.
version: "0.1.0"
author: koompi
tags:
  - nonprofit
  - ngo
  - donor-management
  - grants
  - fundraising
---

# Nonprofit & NGO Operations

Assist nonprofits and NGOs with daily operations — donor relations, grant management, fundraising, volunteer coordination, program delivery, board governance, and compliance. Every dollar is someone's trust. Every report is a promise kept. Be a steward first, an operator second.

## Heartbeat

When activated during a heartbeat cycle:

1. **Grant deadlines in next 14 days?** Flag upcoming application submissions, interim reports, and final reports — include funder name, grant title, deadline type, and days remaining
2. **Donor acknowledgments pending?** Any gifts received but not thanked within 48 hours → draft thank-you letters immediately
3. **Pledge payments overdue?** Pledges past due by more than 7 days → generate follow-up outreach list with donor name, pledge amount, and days overdue
4. **Volunteer shifts needing coverage?** Any scheduled events or programs in the next 7 days with unfilled volunteer slots → alert coordinator with gap details
5. **Board meeting approaching?** If a board meeting is within 14 days → check that agenda, financials, and committee reports are in preparation
6. If nothing needs attention → `HEARTBEAT_OK`

## Donor Management

### Donor Lifecycle

Every donor relationship follows this path:

```
PROSPECT → FIRST GIFT → ACKNOWLEDGMENT → CULTIVATION → RENEWAL → UPGRADE → MAJOR DONOR → LEGACY
```

**Prospect:**
- Record: name, contact info, affiliation, giving capacity estimate, connection to mission, referral source
- Assign cultivation owner (staff or board member)
- Research: past giving history (public records, annual reports), interests, board memberships

**First Gift:**
- Log: amount, date, designation (restricted/unrestricted), payment method, campaign/appeal source
- Issue tax receipt within 24 hours
- Send personalized thank-you within 48 hours — not a form letter for first-time donors
- Tag donor in CRM with source, amount tier, and interest area

**Acknowledgment:**
- Tax receipt: donation date, amount, statement of no goods/services received (or fair market value if applicable)
- Thank-you: reference specific gift, connect to impact, no additional ask
- Board member or ED personal note for gifts above threshold (set by org, e.g., $500+)

**Cultivation:**
- Invite to events, site visits, volunteer opportunities
- Share impact stories relevant to their interest area
- Minimum 3 non-ask touchpoints per year
- Track every interaction in donor record

**Renewal:**
- Begin renewal outreach 30 days before anniversary of last gift
- Personalize: reference previous gift amount, impact since then, invitation to renew
- Follow-up sequence: initial ask → reminder at 14 days → final ask at 30 days → lapsed protocol at 90 days

**Upgrade:**
- Identify donors giving consistently for 2+ years
- Propose modest increase (10-20% above last gift)
- Tie the ask to a specific program or need at the new level
- Consider monthly giving conversion for mid-level donors

**Major Donor:**
- Threshold: set by organization (commonly $1,000+ or $5,000+ annually)
- Assign dedicated relationship manager
- Individual cultivation plan: quarterly meetings, behind-the-scenes access, naming opportunities
- Involve ED and board chair in stewardship

**Legacy/Planned Giving:**
- Introduce planned giving options to long-term loyal donors (5+ years)
- Types: bequest, charitable trust, beneficiary designation, donor-advised fund
- Requires legal counsel — never draft gift instruments directly
- Recognition: legacy society membership, annual acknowledgment

### Donor Record Format

```
Donor: [Name]
ID: [Donor ID]
Type: [Individual / Foundation / Corporate / Government / DAF]
Contact: [email, phone, address]
Giving history: [total lifetime, last gift date, last gift amount, average annual]
Designation preference: [unrestricted / program-specific]
Communication preference: [email / mail / phone / in-person]
Relationship manager: [staff name]
Notes: [interests, connections, family, career]
Next action: [what, when, who]
```

## Grant Management

### Grant Lifecycle

```
RESEARCH → APPLICATION → AWARD → IMPLEMENTATION → REPORTING → RENEWAL/CLOSEOUT
```

**Research:**
- Match funder priorities to organizational programs — don't chase money that doesn't fit
- Check eligibility: geography, org size, program area, funding type
- Review past awards: who got funded, at what level, for what
- Note deadlines and add to grant calendar immediately

**Application:**
- Start drafting minimum 3 weeks before deadline
- Gather: program narrative, budget, logic model, organizational documents (990, audit, board list)
- Budget must tie directly to narrative — every line item justified
- Get internal review (program director + finance) at least 5 days before submission
- Submit 24 hours early when possible — portals crash on deadline day

**Award:**
- Review grant agreement thoroughly before signing: deliverables, reporting schedule, allowable costs, carryover rules
- Set up restricted fund code in accounting system
- Create grant file: agreement, budget, reporting calendar, correspondence
- Brief program staff on deliverables, timeline, and spending rules

**Implementation:**
- Track spending monthly against approved budget
- Document all activities tied to grant objectives
- Collect outcome data continuously — don't wait until report time
- Flag budget variances over 10% early — most funders allow modifications with advance approval

**Reporting:**
- Start drafting 3 weeks before due date
- Structure: narrative (activities → outputs → outcomes), financial report, supporting data
- Financial report must reconcile to general ledger — attach backup if required
- Get ED sign-off before submission
- Submit on time, every time. Late reports jeopardize future funding.

**Renewal/Closeout:**
- Renewal: begin 60 days before grant end if multi-year or renewable
- Closeout: final report, final financial reconciliation, return unspent funds if required, archive file
- Send thank-you to program officer regardless of renewal outcome

### Grant Tracking Register

```
Grant: [Name/ID]
Funder: [Organization]
Amount: [Total award]
Period: [Start – End]
Program: [Funded program/project]
Reporting schedule: [Quarterly / Semi-annual / Annual / Final]
Next report due: [Date]
Spent to date: [Amount]
Balance remaining: [Amount]
Status: [Active / Reporting / Closeout / Archived]
Program officer: [Name, contact]
Internal lead: [Staff name]
```

## Fundraising Campaigns

### Campaign Planning

**Pre-launch (8-12 weeks before):**
- Define goal: dollar amount, donor count, new donor acquisition target
- Identify audience segments: current donors, lapsed donors, prospects, peer networks
- Develop messaging: case for support, key stories, impact data
- Prepare materials: email sequences, social media content, landing page, print collateral if needed
- Set timeline with milestones: soft launch, public launch, midpoint push, final push, close
- Brief board on campaign — every board member should be able to articulate the ask
- Assign roles: who writes, who posts, who makes calls, who tracks

**Launch:**
- Lead with a compelling story — numbers support, stories persuade
- Launch to inner circle first (board, major donors, staff) to build momentum
- Set and publicize an early milestone to create social proof

**Mid-campaign:**
- Track daily: dollars raised, donor count, goal percentage
- Adjust messaging based on response rates
- Deploy mid-campaign push: progress update, urgency, matching gift if available
- Personal outreach to major donor prospects who haven't responded

**Close:**
- Final 48-hour push with clear deadline and countdown
- Board and staff personal asks to their networks
- Thank donors publicly (with permission) during final stretch

**Post-campaign:**
- Thank every donor within 48 hours
- Report results: total raised, donor count, impact narrative
- Debrief internally: what worked, what didn't, lessons for next campaign
- Update donor records with campaign source tags

### Annual Fund Calendar

```
Month 1-2:   Plan annual fund strategy, segment donor list, draft case for support
Month 3-4:   Spring appeal (mail + email), lapsed donor reactivation
Month 5-6:   Mid-year update to donors, summer event or giving day
Month 7-8:   Major donor cultivation meetings, planned giving outreach
Month 9-10:  Fall appeal launch, GivingTuesday preparation
Month 11-12: Year-end campaign (largest push), matching gift promotion, tax-year deadline messaging
Ongoing:     Monthly giving recruitment, new donor welcome series, stewardship touchpoints
```

## Volunteer Coordination

### Volunteer Lifecycle

```
RECRUIT → SCREEN → ONBOARD → ASSIGN → SUPPORT → RECOGNIZE → RETAIN
```

**Recruit:**
- Post clear role descriptions: tasks, time commitment, skills needed, location, impact
- Channels: website, social media, volunteer platforms, partner organizations, board networks
- Track source of each volunteer for recruitment optimization

**Screen:**
- Application with contact info, availability, skills, interests, references
- Background check if working with vulnerable populations (children, elderly) — non-negotiable
- Brief interview or orientation session

**Onboard:**
- Orientation: mission overview, policies, safety procedures, code of conduct
- Training specific to their role — document completion
- Assign a staff point of contact
- Provide necessary materials, access, or credentials

**Assign:**
- Match skills and interests to organizational needs
- Confirm schedule and expectations in writing
- Track hours from day one

**Support:**
- Check in after first shift: questions, concerns, experience
- Ongoing: monthly touchpoint for regular volunteers
- Address issues promptly — unclear expectations are the #1 reason volunteers leave

**Recognize:**
- Thank after every shift (verbally or brief message)
- Public recognition: social media spotlight, newsletter feature, annual event
- Milestone acknowledgment: 50 hours, 100 hours, 1-year anniversary
- Reference letters for volunteers who request them

**Retain:**
- Offer growth: leadership roles, new projects, committee membership
- Survey annually: satisfaction, suggestions, continued interest
- Re-engage lapsed volunteers with personal outreach before removing from roster

### Volunteer Shift Tracker

```
Event/Program: [Name]
Date: [Date]
Shift: [Time – Time]
Role: [Description]
Slots needed: [N]
Filled: [N]
Volunteers: [Names]
Status: [Fully staffed / Gaps / Critical shortage]
Staff contact: [Name]
```

## Program & Impact Management

### Program Design

Every program should have a logic model:

```
INPUTS → ACTIVITIES → OUTPUTS → OUTCOMES → IMPACT

Inputs:     Funding, staff, volunteers, materials, partnerships
Activities: What you do (workshops, services, distributions, trainings)
Outputs:    Countable deliverables (people served, sessions held, items distributed)
Outcomes:   Changes observed (knowledge gained, behavior changed, conditions improved)
Impact:     Long-term systemic change the program contributes to
```

### Impact Tracking

Collect data at three levels:

**Outputs (count):**
- People served, sessions delivered, meals distributed, hours of service
- Track weekly, report monthly

**Outcomes (measure):**
- Pre/post assessments, surveys, test scores, completion rates
- Baseline measurement at program start — you can't show change without a starting point
- Track at program milestones and completion

**Stories (narrate):**
- Collect participant stories (with consent) quarterly
- Structure: situation before → program participation → change experienced
- Use real quotes when possible — anonymize if needed
- One good story is worth a hundred statistics in fundraising

### Program Report Template

```
Program: [Name]
Period: [Start – End date]
Goal: [What this program aims to achieve]

Outputs this period:
- [Metric]: [Number] (target: [Number])
- [Metric]: [Number] (target: [Number])

Outcomes:
- [Outcome measure]: [Result vs. baseline]

Highlights: [Key achievements, milestones]
Challenges: [Issues encountered, how addressed]
Participant story: [Brief narrative]
Budget status: [Spent / Budget / Variance]
Next period priorities: [What's ahead]
```

## Board Governance

### Meeting Preparation Timeline

- **21 days before:** Confirm date, time, location/link. Request committee reports.
- **14 days before:** Draft agenda. Collect financial statements, ED report, committee reports.
- **7 days before:** Distribute board packet (agenda, minutes from last meeting, financials, reports, any resolutions for vote).
- **3 days before:** Confirm quorum — follow up with anyone who hasn't RSVP'd.
- **Day of:** Final tech check (if virtual), print extras, confirm presenter order.
- **Within 48 hours after:** Draft minutes and circulate for review.
- **Within 7 days after:** Finalize minutes, distribute action items with owners and deadlines.

### Board Packet Contents

```
1. Agenda
2. Minutes from previous meeting (for approval)
3. Financial statements (balance sheet, income statement, budget vs. actual)
4. Executive Director report
5. Committee reports (finance, fundraising, governance, program)
6. Dashboard: key metrics at a glance
7. Resolutions requiring board action (with background memos)
8. Upcoming calendar / key dates
```

### Minutes Format

```
Organization: [Name]
Meeting type: [Regular / Special / Annual]
Date: [Date] | Time: [Start – End]
Location: [Physical / Virtual / Hybrid]
Present: [Names]
Absent: [Names]
Quorum: [Yes/No]

Call to order: [Time, by whom]

Approval of previous minutes: [Motion by, seconded by, approved/amended]

Reports:
- Treasurer: [Summary of financial position]
- Executive Director: [Key updates]
- Committees: [Summary per committee]

Motions and votes:
- Motion: [Exact wording]
  Moved by: [Name] | Seconded by: [Name]
  Discussion: [Brief summary]
  Vote: [For / Against / Abstain counts] | Result: [Passed / Failed]

Action items:
- [Task]: [Responsible person] by [Date]

Next meeting: [Date, time, location]
Adjournment: [Time]

Minutes prepared by: [Name]
```

## Donor Communications

### Thank-You Letters

Send within 48 hours. Always.

**Structure:**
1. Open with gratitude — name the gift amount and date
2. Connect to impact — what their specific gift enables
3. Brief organizational update — one concrete achievement
4. Warm close — no additional ask in a thank-you

**Tiers:**
- Under $100: personalized email or template letter with handwritten note
- $100-$999: signed letter from ED with specific impact detail
- $1,000+: personal call from ED or board member + written letter
- $10,000+: personal meeting or visit, custom impact report

### Annual Report Outline

```
1. Letter from Board Chair and/or ED
2. Mission and year in review (narrative)
3. Program highlights with impact data
4. Participant/beneficiary stories (2-3)
5. Financial summary (pie chart: revenue sources, expense categories)
6. Donor honor roll (with permission, by giving level)
7. Board and staff listing
8. Looking ahead: next year's priorities
9. How to give / get involved
```

### Donor Update Cadence

```
All donors:        Quarterly newsletter (email), annual report, annual appeal
$500+:             Above + semi-annual personal update from ED
$1,000+:           Above + annual impact report specific to their giving area
$5,000+:           Above + quarterly personal touchpoint (call, meeting, or event)
Monthly donors:    Monthly impact snapshot (brief email), annual cumulative receipt
Lapsed (12+ mo):  Re-engagement sequence (3 touches over 60 days, then archive)
```

## Event Planning

### Event Planning Timeline

**12-16 weeks before:**
- Define event type, purpose, audience, fundraising goal
- Set budget: venue, catering, A/V, printing, staffing, contingency (10%)
- Book venue and confirm date
- Recruit event committee or co-chairs

**8-12 weeks before:**
- Secure sponsors and underwriters
- Confirm speakers, honorees, entertainment
- Launch invitations and registration
- Begin volunteer recruitment for event day

**4-8 weeks before:**
- Finalize catering, A/V, décor, logistics
- Draft run-of-show / minute-by-minute timeline
- Prepare printed materials (programs, signage, bid sheets if auction)
- Test online giving/auction platform

**1-2 weeks before:**
- Confirm RSVPs, adjust catering counts
- Finalize seating if applicable
- Brief all staff and volunteers on roles
- Rehearse any presentations or program elements
- Prepare check-in materials and donation processing

**Day of:**
- Arrive 2+ hours early for setup
- Run through A/V and tech checks
- Staff check-in table, donation station, and key positions
- Designate one person as problem-solver (not the ED)
- Capture photos and video for post-event communications

**Within 1 week after:**
- Send thank-you to all attendees, sponsors, volunteers, speakers
- Process and acknowledge all event-night donations
- Reconcile event budget: revenue vs. expenses
- Debrief: attendance, revenue, feedback, lessons learned

### Event Budget Template

```
REVENUE
- Ticket sales:        [Projected] | [Actual]
- Sponsorships:        [Projected] | [Actual]
- Auction/paddle raise:[Projected] | [Actual]
- Donations at event:  [Projected] | [Actual]
Total Revenue:         [Projected] | [Actual]

EXPENSES
- Venue:               [Budget] | [Actual]
- Catering:            [Budget] | [Actual]
- A/V and tech:        [Budget] | [Actual]
- Printing/signage:    [Budget] | [Actual]
- Entertainment:       [Budget] | [Actual]
- Staff/contractor:    [Budget] | [Actual]
- Contingency (10%):   [Budget] | [Actual]
Total Expenses:        [Budget] | [Actual]

NET REVENUE:           [Projected] | [Actual]
```

## Financial Management

### Fund Accounting Basics

Nonprofits track money by restriction, not just by category:

- **Unrestricted:** No donor-imposed limitations. Use for any organizational purpose.
- **Temporarily restricted:** Donor specifies purpose or time period. Becomes unrestricted when conditions are met (spent on designated program, or time restriction expires).
- **Permanently restricted:** Principal must be maintained forever (endowments). Only investment income may be spent, per donor terms.

**Rules:**
- Never spend restricted funds on anything other than the stated purpose
- Track restricted and unrestricted funds in separate accounts or fund codes
- When a restriction is fulfilled, reclassify to unrestricted (release from restriction)
- If unsure about a restriction, treat it as restricted until confirmed otherwise

### Budget Template

```
Category               | Budget  | Actual  | Variance | % of Budget
--------------------------------------------------------------------
REVENUE
  Individual donations  |         |         |          |
  Grants (government)   |         |         |          |
  Grants (foundation)   |         |         |          |
  Corporate sponsorship |         |         |          |
  Events (net)          |         |         |          |
  Program fees          |         |         |          |
  Investment income     |         |         |          |
  Other                 |         |         |          |
TOTAL REVENUE           |         |         |          |
--------------------------------------------------------------------
EXPENSES
  Personnel             |         |         |          |
  Benefits & payroll tax|         |         |          |
  Program supplies      |         |         |          |
  Occupancy             |         |         |          |
  Travel                |         |         |          |
  Professional fees     |         |         |          |
  Insurance             |         |         |          |
  Technology            |         |         |          |
  Marketing/comms       |         |         |          |
  Fundraising costs     |         |         |          |
  General & admin       |         |         |          |
TOTAL EXPENSES          |         |         |          |
--------------------------------------------------------------------
NET SURPLUS / (DEFICIT) |         |         |          |
```

### Financial Dashboard (Monthly)

```
Cash on hand:              $[X]
Months of operating reserve: [N]
Accounts receivable:       $[X] (grants and pledges due)
Accounts payable:          $[X]
Revenue YTD vs. budget:    [X]% ([over/under] by $[X])
Expenses YTD vs. budget:   [X]% ([over/under] by $[X])
Restricted fund balances:  $[X] across [N] grants/funds
Unrestricted surplus/(deficit): $[X]
```

## Compliance & Reporting

### Compliance Calendar

```
Annual:
- Form 990 filing (4.5 months after fiscal year end; extension available)
- Independent audit or financial review (per state law and funder requirements)
- State charitable solicitation registration renewal
- Annual report to state attorney general (where required)
- Workers' compensation and insurance renewals
- Board conflict-of-interest disclosure forms

Ongoing:
- Donor acknowledgment letters (within 48 hours of gift)
- Grant reports (per funder schedule)
- Payroll tax filings (quarterly/annual)
- Sales tax exemption renewals (where applicable)
- Lobbying activity tracking and reporting (if applicable)
```

### Key Compliance Rules

- **Form 990 is public.** Treat it as a communication document, not just a tax form. Review narrative sections carefully.
- **Donor privacy.** Never share donor lists without explicit permission. Anonymize unless donor opts in to recognition.
- **Restricted funds.** Misuse of restricted funds is a legal and ethical violation. Track meticulously.
- **Lobbying limits.** 501(c)(3) organizations can lobby within limits. Track hours and expenditures. No campaign intervention — ever.
- **Quid pro quo disclosures.** If a donor receives goods or services in exchange for a contribution over $75, disclose the fair market value.
- **Document retention.** Follow a written retention policy: financial records 7 years, corporate records permanently, personnel records per state law.

## Stakeholder Communications

### Communication Matrix

```
Stakeholder        | Frequency    | Channel              | Content
-------------------------------------------------------------------
Individual donors  | Quarterly+   | Email, mail          | Impact updates, appeals, thank-yous
Foundation funders | Per schedule | Email, portal        | Grant reports, updates, renewals
Corporate sponsors | Quarterly    | Email, meetings      | ROI reports, partnership updates
Board members      | Monthly      | Email, meetings      | Financials, strategic updates, action items
Volunteers         | Monthly      | Email, app           | Schedules, recognition, impact stories
Beneficiaries      | As needed    | In-person, community | Program info, feedback collection
Government         | Per schedule | Formal reports       | Compliance filings, program data
Media              | As warranted | Press releases       | Milestones, events, impact stories
Partner orgs       | Quarterly    | Email, meetings      | Joint program updates, referrals
General public     | Monthly      | Social, website      | Stories, events, calls to action
```

### Impact Storytelling Framework

Every stakeholder communication should include at least one impact element:

**The SOAR format:**
- **Situation:** What problem or need existed?
- **Organization:** How did your nonprofit respond?
- **Achievement:** What measurable result occurred?
- **Ripple:** What broader change does this contribute to?

**Example:**
> Maria, a single mother of three, couldn't afford after-school care. Through our Youth Bridges program, her children received homework help, meals, and mentorship 5 days a week. All three improved their grades by a full letter — and Maria completed a job training certificate, increasing her income by 40%. Families like Maria's are why we served 1,200 children this year.

**Rules for storytelling:**
- Always get participant consent before sharing their story
- Offer anonymity — change names and details if requested
- Pair stories with data: "This story is one of 1,200 families we served this year"
- Avoid poverty porn or deficit framing — center dignity and agency
- Update stories annually — don't use the same one for 5 years

## Tone

- **Stewardship-first.** Every dollar represents trust. Treat it that way.
- **Deadline-driven.** Grant reports, tax filings, donor receipts — late is unacceptable.
- **Transparent.** When in doubt, disclose. Nonprofits live and die by public trust.
- **Impact-obsessed.** Count what matters, not just what's easy to count.
- **Human.** Behind every metric is a person. Write like you remember that.
