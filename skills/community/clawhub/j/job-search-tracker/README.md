# Job Search Tracker

An OpenClaw skill that tracks job applications from discovery to offer, flags stale applications, and helps with follow-up emails, cover letters, salary negotiation, and interview prep.

**Current version: 1.1.2**

## What's new in 1.1.2

- Rewrote the **Data Handling and Privacy** section to accurately describe tool usage (rather than understating it)
- Added a **Permissions and Privacy** section to this README so users see the scope of access before installing
- Narrowed the activation triggers in `description` to reduce over-activation on generic email or calendar phrases

See [CHANGELOG.md](CHANGELOG.md) for the full release history.

## What it does

- **Tracks applications** in a single markdown file with status, contacts, timeline, salary, resume version, and follow-up dates
- **Detects stale applications** and flags anything needing attention (no response in 7+ days, overdue follow-ups, upcoming interviews)
- **Generates a dashboard** with pipeline counts, recent activity, and actionable next steps
- **Drafts follow-up emails, cover letters, and thank-you notes** using context from your tracker
- **Recommends the best resume variant** for each posting (1.1.0)
- **Tone-checks your drafts** for desperate or templated language (1.1.0)
- **Supports salary negotiation** with counter-offer analysis and drafting (1.1.0)
- **Preps you for interviews** with company research briefs, mock questions, and talking points
- **Integrates with Gmail** to scan for application confirmations and pull recruiter email context
- **Integrates with LinkedIn** to track Easy Apply submissions and research companies/contacts

All integrations are optional. The skill works well with just what you tell it directly.

## Install

```bash
openclaw skill install chris-openclaw/job-search-tracker
```

## Example prompts

- "I just applied to a Product Manager role at Stripe. Track it."
- "What needs attention in my job search?"
- "Which resume should I send for this posting?"
- "Does this follow-up email sound desperate?"
- "I have an interview with Notion on Thursday. Prep me."
- "Draft a follow-up email for the Datadog recruiter."
- "I got an offer from Linear — help me think through the counter."
- "Check my email for any new application confirmations."
- "I got rejected from Shopify."

## How it stores data

Everything lives in `applications.md` in your working directory. Each company gets its own section with status, contacts, timeline, notes, and follow-up info. The file is plain markdown, so you can read and edit it yourself anytime.

Resume variants live in a sibling `resumes/` directory if you want the recommender feature.

## Permissions and Privacy (read before installing)

This skill instructs the assistant to use whichever of the following tools you have connected — it does not bundle them, but it will reach for them when relevant:

- **Gmail / email tools**: search for application confirmations, recruiter messages, interview scheduling, and offer details. Touches inbox content. Connect only if you're comfortable with assistant-mediated reads of your job-search email threads.
- **LinkedIn / browser automation**: track LinkedIn Easy Apply submissions, look up companies and recruiters, view "My Jobs > Applied." Touches your LinkedIn session. Connect only if you're comfortable with that scope.
- **Web search**: look up companies for interview prep when LinkedIn is not available. No personal data is sent.
- **Local file write**: creates and updates `applications.md`, `resumes/` (if used), and any drafts in your current working directory. No writes outside that directory.

**What the skill itself does NOT do**: it doesn't transmit data to its author, ClawHub, or any third party; it has no telemetry or background processes; it does not store credentials. Any data leaving your machine does so through the tools listed above, under your own permissions.

**Confirmation rule**: before adding any application detected from Gmail or LinkedIn into your tracker, the assistant will surface the find and wait for your explicit confirmation. Silent ingestion is not allowed.

**Tracker-only mode**: if you'd rather not connect Gmail or LinkedIn, just don't. Every workflow still functions from what you tell the assistant directly. The integrations are a convenience layer, not a requirement.
