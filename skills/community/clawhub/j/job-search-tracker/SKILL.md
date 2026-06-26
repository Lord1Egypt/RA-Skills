---
name: job-search-tracker
version: 1.1.2
description: "Use this skill when someone is actively managing a job search and references applications, interviews, offers, or recruiter communication. Specific triggers: 'I applied to [company],' 'just submitted an application,' 'track this job,' 'job search dashboard,' 'what jobs have I applied to,' 'any responses from [company] yet,' 'haven't heard back from [company],' 'prep me for the [company] interview,' 'draft a cover letter for [company/role],' 'write a follow-up email to [company/recruiter],' 'thank-you note for the [company] interview,' 'got rejected from [company],' 'got an offer from [company],' 'help me negotiate the [company] offer,' 'salary negotiation,' 'which resume should I send for [posting],' 'does this [draft] sound desperate or templated,' or any message that explicitly names a company in a hiring context. Do NOT trigger on general productivity questions, calendar requests, or unrelated email tasks. Covers: application tracking in a local markdown file, stale-application detection, follow-up and cover-letter drafting with tracker context, interview prep, salary negotiation analysis and counter-offer drafting, tone checks on user drafts, resume-variant recommendations, and optional Gmail/LinkedIn lookups (user-mediated, see Data Handling)."
metadata:
  openclaw:
    emoji: 🎯
---

# Job Search Tracker

A complete job search command center. Tracks every application from discovery to offer, integrates with Gmail and LinkedIn for context, flags stale applications that need follow-up, and helps draft cover letters, follow-up emails, and interview prep materials.

## Why this exists

Job searching while juggling other responsibilities is chaotic. You apply to 30 places, lose track of which ones you followed up on, forget the recruiter's name, and can't remember which version of your resume you sent. This skill keeps it all in one place and does the busywork for you.

---

## The Applications File

All application data lives in a single markdown file: `applications.md` in the current working directory (or wherever the user specifies). This file is the source of truth for the entire job search.

### File structure

```markdown
# Job Search Tracker

_Last updated: YYYY-MM-DD_
_Active applications: X | Interviews: X | Offers: X | Closed: X_

---

## [Company Name] - [Role Title]
- **Status**: [Applied | Screening | Interviewing | Final Round | Offer | Accepted | Rejected | Withdrawn | Ghosted]
- **Date Applied**: YYYY-MM-DD
- **Posting URL**: [link]
- **Salary Range**: [what's listed or discussed]
- **Resume Version**: [which resume was sent]
- **Cover Letter**: [yes/no, and which version or key angle used]
- **Source**: [LinkedIn Easy Apply | Company Site | Referral | Recruiter Outreach | Job Board]

### Contacts
- [Name] - [Title] (e.g., "Sarah Chen - Senior Recruiter") - [email if known]
- [Name] - [Title] - [email if known]

### Timeline
- YYYY-MM-DD: Applied via [source]
- YYYY-MM-DD: [Event - e.g., "Phone screen with Sarah Chen", "Received coding assessment", "Sent follow-up email"]

### Notes
[Freeform notes - anything relevant about the role, company, conversations, gut feelings, red flags, compensation details discussed]

### Follow-up
- **Next action**: [what needs to happen next]
- **Due by**: [date]
- **Last contact**: [date of most recent communication]

---
```

Each company gets its own section with the `## Company - Role` header. Sections are ordered by status priority: active applications first (Interviewing > Screening > Applied), then closed ones (Offers > Accepted > Rejected > Withdrawn > Ghosted) at the bottom.

### Creating the file

If `applications.md` doesn't exist when the user asks to track something, create it with the header and their first application. Don't make a big deal of setup; just start tracking.

### Updating entries

When the user reports a status change ("I heard back from Stripe" or "got rejected from Google"), update the relevant section: change the status, add a timeline entry with today's date, and update the follow-up section. If they mention a new contact name, add it to Contacts.

---

## Gmail Integration

This skill works best when Gmail access is available (via MCP tools, the Gmail skill, or IMAP). When email tools are available, use them. When they're not, work with whatever the user tells you manually.

### Auto-detecting applications

When the user asks you to scan their email for applications (or when doing a periodic check-in):

1. Search Gmail for recent application-related emails using queries like:
   - `subject:"application received" OR subject:"application confirmed" OR subject:"thank you for applying" OR subject:"we received your application"`
   - `from:notifications@linkedin.com subject:"application"`
   - `subject:"next steps" from:recruiting OR from:talent OR from:careers`
2. For each result, extract: company name, role title, date, and any recruiter names mentioned
3. Cross-reference against `applications.md` to avoid duplicates
4. Present new finds to the user: "I found 3 applications in your email that aren't in your tracker yet. Want me to add them?"
5. Only add entries the user confirms

### Pulling context on demand

When the user asks about a specific company or the skill needs more context:

1. Search Gmail for threads involving that company name
2. Surface relevant emails: recruiter messages, interview scheduling, assessment links, offer details
3. Summarize what the email trail shows (last contact date, who reached out, what stage it suggests)

---

## LinkedIn Integration

LinkedIn integration works through browser automation or the LinkedIn skill/MCP if available. Since LinkedIn access can be unreliable, design all features to work without it and treat LinkedIn data as a bonus layer.

### Tracking applications

When the user mentions applying through LinkedIn or asks to check their recent applications:

1. If browser tools are available, navigate to LinkedIn's "My Jobs" > "Applied" tab
2. Extract recent applications: company, role, date applied
3. Cross-reference against `applications.md`
4. Present new ones for confirmation before adding

### Research on demand

When adding a new application or prepping for an interview:

1. Look up the company on LinkedIn for: company size, industry, recent news/posts, key people in the department
2. Check if the user has any connections at the company
3. Look up the hiring manager or recruiter if named
4. Summarize findings in a research brief

If LinkedIn isn't accessible, fall back to web search for company research. The research should happen regardless; LinkedIn is just one source.

---

## Resume Recommender

Many users keep multiple resume variants tailored to different job types (e.g., "engineering-focused," "leadership-focused," "generalist"). This skill can suggest the best variant for a given posting.

### Storing resume variants

Resumes live in a `resumes/` directory alongside `applications.md`. Each variant is a markdown or text file named for its slant:

```
resumes/
  engineering-focused.md
  leadership-focused.md
  generalist.md
```

Each file should start with a one-paragraph self-description that summarizes the angle it takes. The skill reads these descriptions to make recommendations. It does not need the full resume content for matching, just the description block at the top.

### Recommending a variant

When the user adds a new application, asks "which resume should I send?", or pastes a job posting:

1. Read the job posting (from URL, pasted text, or the tracker entry)
2. Read each resume's self-description from `resumes/`
3. Extract key signals from the posting: required skills, seniority level, team size, company size, work style cues (remote/hybrid/onsite, IC vs management)
4. Recommend the variant whose self-description best matches those signals
5. Present the recommendation with a one-line rationale: "Suggested: leadership-focused.md (the posting emphasizes managing a cross-functional team and reporting to a VP)"
6. Offer to log the choice to the tracker entry's `Resume Version` field

If no `resumes/` directory exists, prompt the user once: "I don't see saved resume variants. Want to set up the `resumes/` folder, or just track which version you sent each time?" Don't badger after the initial prompt; respect "no" the first time.

---

## Proactive Reminders and Follow-ups

This is one of the most valuable features. Job seekers lose opportunities by not following up.

### Stale application detection

When the user opens their tracker or asks "what needs attention", scan all active applications and flag:

- **No response in 7+ days after applying**: Suggest sending a follow-up email
- **No response in 3+ days after an interview**: Suggest a thank-you note or check-in
- **Scheduled interview coming up in 48 hours**: Prompt for interview prep
- **No activity in 14+ days on any active application**: Suggest checking in or marking as Ghosted
- **Follow-up due date passed**: Highlight overdue items

### Dashboard view

When the user asks for their job search status, dashboard, or overview, generate a summary:

```markdown
# Job Search Dashboard
_As of YYYY-MM-DD_

## Needs Attention (X items)
- **[Company] - [Role]**: No response in 10 days. Consider following up.
- **[Company] - [Role]**: Interview tomorrow. Run interview prep?
- **[Company] - [Role]**: Follow-up was due 2 days ago.

## Pipeline Summary
- Actively interviewing: X
- Waiting to hear back: X
- Applied recently (< 7 days): X
- Total active: X
- Closed this month: X (Y rejected, Z withdrawn)

## Recent Activity
- [Date]: [Event summary]
- [Date]: [Event summary]
- [Date]: [Event summary]

## Stats
- Applications this week: X
- Response rate: X%
- Average time to first response: X days
```

---

## Drafting Help

The skill helps draft outreach materials tailored to each specific application. The key value here is that the skill has all the context from the tracker -- it knows what role the user applied for, who they've been talking to, and what's happened so far.

### Cover letters

When the user asks for a cover letter:

1. Ask for the job posting URL or description (or pull it from the tracker if already saved)
2. Ask which resume version they're using (or check the tracker)
3. Draft a cover letter that:
   - Opens with something specific about the company, not generic praise
   - Connects the user's actual experience to the role's requirements
   - Keeps it to one page, three to four paragraphs
   - Avoids cliches ("passionate about," "excited to bring my skills")
   - Sounds like a real person wrote it, not a template
4. Save a note in the tracker about which angle the cover letter took

### Follow-up emails

When following up on an application or after an interview:

1. Check the tracker for context: when they applied, who they've talked to, what stage they're in
2. Draft an email that:
   - References the specific role and conversation
   - Adds something of value (a thought from the interview, a relevant article, a brief example of their work)
   - Is short and direct (under 150 words for follow-ups)
   - Has a clear ask or next step
3. After presenting the draft, always offer to log this follow-up in the tracker: "Want me to add this to your timeline and update the follow-up date?"
4. If the user confirms (or doesn't object), add a timeline entry and update the follow-up section with the new date

### Thank-you notes

After an interview:

1. Ask who they met with and what was discussed (or pull from tracker notes)
2. Draft a note that:
   - References something specific from the conversation
   - Reinforces fit for the role
   - Is genuine, not formulaic
3. One thank-you per interviewer if they met multiple people, with slight variations so they don't look identical if compared

### Tone check on user drafts

When the user pastes their own draft and asks for a check (or says "does this sound desperate," "is this templated," "does this sound okay"), run a quick tone pass before they send.

**Flag categories**

- **Desperate signals**: "I'll do anything," "any role," "please consider me," stacked over-thanking ("thank you so much for your time" appearing twice), excessive flexibility statements ("I'm open to anything," "happy to start whenever")
- **Templated signals**: openings like "I hope this email finds you well," "I am writing to," generic praise of the company ("a leader in the industry," "world-class team"), zero specifics pulled from the actual job posting or prior conversation
- **Negative framing**: apologizing for gaps, leading with weakness, "I know I'm a long shot," "I may not have all the qualifications but"
- **Length issues**: follow-ups over 200 words, cover letter paragraphs over 5 sentences, opening paragraph that doesn't get to the point in 2 sentences

**Output format**

```
Tone read: [Tight | Mostly fine, some flags | Needs work]

Flags found:
1. [Category] — "[exact phrase from draft]" — why it lands flat
2. ...

Suggested revisions:
- "[phrase]" → "[better phrase]"
- ...
```

If the draft is already tight, say so directly: "Reads well. Nothing to fix. Ready to send."

Do not rewrite the entire draft unless the user asks. The goal is a targeted edit, not a full rewrite that erases their voice.

---

## Interview Prep

When the user has an upcoming interview or asks to prep for one:

### Company research brief

Generate a one-page brief covering:
- What the company does (in plain language, not marketing copy)
- Recent news, product launches, or challenges
- Company size, funding stage, growth trajectory
- Culture signals (from job posting language, Glassdoor, LinkedIn posts)
- Key people they might meet (from LinkedIn or the tracker's contacts)

### Role-specific prep

Based on the job posting:
- Key skills/requirements they should be ready to demonstrate
- Likely question themes (behavioral, technical, case-based)
- Their strongest talking points mapped to the role's requirements
- Potential concerns a hiring manager might have (gaps, career pivots, missing skills) and how to address them
- Questions the user should ask the interviewer

### Mock questions

Generate 8-10 likely interview questions:
- 3-4 behavioral ("Tell me about a time when...")
- 2-3 role-specific or technical
- 2-3 situational ("How would you handle...")

For each question, provide a brief outline of a strong answer structure, not a full script. The user should sound like themselves, not like they memorized something.

---

## Salary Negotiation

When the user reports an offer (triggers like "got an offer," "they made me an offer," "offer letter came in," "they came in at X"), shift into negotiation support mode.

### First-pass triage

1. Update the tracker: status → Offer, add timeline entry with the offer details
2. Pull context from the entry: what range was discussed at application or screen, what was on the posting, how the conversation progressed
3. Ask three quick questions if not already known:
   - What's the base offer, and any equity, sign-on, or bonus structure?
   - What was the original range they signaled?
   - How does this compare to your target and your floor?

### Counter-offer analysis

Based on tracker context:

- Calculate deltas: offer vs. low/mid/high of the posted range, vs. the user's target, vs. their floor
- Identify which components have negotiation room. Base usually has the most. Sign-on is often easier to move than base because it doesn't affect headcount budget. Equity is frequently flexible at senior levels. Vacation, start date, and remote/onsite are sometimes negotiable.
- Suggest a specific counter, not a vague "ask for more." Example: "Counter at $X base + $Y sign-on. That's the high end of their stated range plus a sign-on that closes the gap to your target."

### Counter-offer draft

If the user wants help responding:

1. Draft a short, professional message that:
   - Opens with one sentence of genuine enthusiasm about the role (not gushing)
   - States the counter clearly and specifically
   - Anchors the counter in something concrete: market data, the original posted range, the scope of the role, or a competing interest
   - Leaves room to land somewhere in between
   - Does not apologize for negotiating
2. Avoid ultimatum framing unless the user explicitly wants to walk
3. Save the draft to the tracker timeline

### Things to flag

- **Exploding offers** (deadline under 48 hours): a pressure tactic. Suggest the user ask for more time. "I want to give this the consideration it deserves; could we extend the deadline by a few days?"
- **Verbal-only offers**: prompt the user to get it in writing before negotiating
- **Below-range offers**: if the offer is below the posting's stated range, surface that directly. It's a meaningful signal about how the relationship will go.
- **Total comp framing**: if the company emphasizes total comp heavily (equity-weighted, OTE-weighted), break it down to what's actually guaranteed cash

---

## Common Workflows

**"I just applied to a job"**
1. Ask for company, role, posting URL, how they applied, salary range if listed
2. Create or update the entry in `applications.md`
3. Set a follow-up reminder for 7 days out
4. Offer to draft a connection request or follow-up plan

**"Check my email for new applications"**
1. Search Gmail for application confirmations since last check
2. Present findings, add confirmed ones to tracker
3. Run a quick stale-application scan while you're at it

**"I have an interview with [Company] on [Date]"**
1. Update the tracker status to Interviewing, add timeline entry
2. Ask who they're meeting with
3. Offer to generate a company research brief and mock questions
4. Set a reminder for the day before

**"What's my job search looking like?"**
1. Read `applications.md`
2. Generate the dashboard view
3. Flag anything needing attention
4. Offer to help with the highest-priority items

**"I got rejected from [Company]"**
1. Update status to Rejected, add timeline entry
2. Brief empathy (one line, not a pep talk)
3. Suggest: "Want to draft a gracious response? Sometimes it keeps the door open for future roles."
4. Move on to what's still active

**"I got an offer"**
1. Update status to Offer, add timeline entry with offer details (base, equity, sign-on, deadline)
2. Pull tracker context: original range, conversations, what was promised
3. Run counter-offer analysis: gap to target, which components have room
4. Offer to draft a counter and log it to the timeline
5. Flag any pressure tactics (exploding offer, verbal-only, below-range)

**"Which resume should I send?"**
1. Read the posting (URL, pasted text, or tracker entry)
2. Read each resume's self-description from `resumes/`
3. Recommend the best-fit variant with a one-line rationale
4. Offer to log the choice in the tracker

**"Does this sound desperate / templated?"**
1. Run the tone check pass on the pasted draft
2. Flag specific phrases, not the whole draft
3. Suggest targeted revisions (don't rewrite top to bottom unless asked)

---

## Data Handling and Privacy

Be honest with the user about what this skill does. It directs the assistant to use tools the user has connected (Gmail, LinkedIn, browser automation, web search) when those tools are available. This skill does not bundle or ship those tools — it instructs the assistant to invoke whichever ones the user has authorized. The data those tools touch is real and sensitive: emails, recruiter contacts, salary figures, offer details, and personal employment history.

The skill itself does not transmit data, run background processes, or persist anything outside the user's working directory. What it directs the assistant to do, the user can see and stop at any time.

**Data scope and consent rules**

- **Local storage by the skill**: `applications.md`, `resumes/`, drafts, dashboards, and any generated documents are written to the user's current working directory. The skill does not write data anywhere else.
- **Tool-mediated reads**: When the skill instructs the assistant to search Gmail, browse LinkedIn, or run a web search, those requests go through tools the user has explicitly connected, under the user's own credentials and permissions. Revoking access to a tool stops the related behavior.
- **Confirmation before writes from external sources**: When the assistant finds candidate applications via Gmail or LinkedIn, it must present the findings to the user and wait for explicit confirmation before adding entries to the tracker. Silent ingestion is not allowed.
- **Sensitive fields stay scoped**: Salary figures, offer details, and recruiter contact information belong in the tracker file. The assistant should not paste these into drafts, summaries, or third-party-bound messages unless the user has asked for that specific output.
- **No destructive operations without consent**: The assistant must not delete entries, overwrite notes, or modify resumes without explicit user confirmation.
- **No telemetry by the skill**: The skill does not collect or transmit usage data, file contents, or any other information back to its author, ClawHub, or any third party. (Connected tools may have their own logging — the user should consult those tools' policies.)

**What a cautious user should know before installing**

This skill is most useful when Gmail and LinkedIn tools are connected, but those connections are not required. Users uncomfortable with broad Gmail or LinkedIn access can use the skill in tracker-only mode by simply not connecting those tools — the assistant will then work from what the user tells it directly, and every workflow above still functions.

---

## Important Notes

- The tracker is the user's data. Don't delete entries or overwrite notes without asking.
- When in doubt about a status change, ask: "Should I mark this as [status]?"
- Keep the emotional temperature right. Job searching is stressful. Be practical and supportive without being syrupy. A rejection is a data point, not a crisis; an offer is exciting, not a reason for five paragraphs of congratulations.
- Gmail and LinkedIn access depend on what tools are available. The skill should work well even with zero integrations, just from what the user tells you directly. The integrations are a bonus, not a requirement.
- Respect privacy. Application data, salary information, and recruiter names are sensitive. Don't include them in any outputs beyond the tracker file itself.
