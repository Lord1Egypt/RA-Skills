# Katelynn Lead Gen

> A full-cycle lead generation and personalized outreach skill for AI agents.
> Built by [gerika.ai](https://gerika.ai) · Open source under MIT License.

---

## What Katelynn Does

**Katelynn Lead Gen** is an AI agent skill that takes a target customer profile and delivers
a ready-to-use list of qualified prospects — each with a personalized outreach message.

Give Katelynn:
- Your **Ideal Customer Profile** (ICP): who you want to reach
- Your **Value Proposition**: what you offer and why they'd care
- Your **Outreach Goal**: the one action you want them to take
- Your **Channel**: email, LinkedIn DM, or both

Katelynn returns:
- A **leads table** with name, title, company, contact info, and research hook
- **Personalized outreach drafts** for each lead (email subjects + body, or LinkedIn DMs)
- A **summary** with research quality notes and next steps
- Exportable **CSV or Markdown** output via the included formatting script

---

## Why It Works

Most cold outreach fails because it's generic. Katelynn is designed around one core principle:
**lead with them, not with you.** Every message opens with something specific and genuine about
the prospect before ever mentioning your product.

---

## Installation

### Via ClawHub.AI
Search for **"Katelynn Lead Gen"** on [ClawHub.AI](https://clawhub.ai) and click Install.

### Via GitLab / Manual
```bash
git clone https://gitlab.com/gerika-ai/skills/katelynn-lead-gen.git
```

Then add the skill to your agent's skills directory and reference `SKILL.md` in your agent config.

### Via .skill file
Download `katelynn-lead-gen.skill` from the [Releases](../../releases) page and install it
in your Claude Code or Cowork environment by copying it to your skills folder.

---

## File Structure

```
katelynn-lead-gen/
├── SKILL.md                    # Core skill instructions (loaded by agent)
├── LICENSE                     # MIT
├── README.md                   # This file
├── references/
│   ├── icp-research.md         # Research tactics and source list
│   └── copywriting.md          # Message frameworks and tone guide
├── scripts/
│   └── format_output.py        # Export leads + messages to CSV or Markdown
└── evals/
    └── evals.json              # Test cases for skill validation
```

---

## Usage Example

**User prompt to agent:**
> "Find me 10 leads for our AI customer support tool. Target B2B SaaS companies with
> 20-100 employees that are actively hiring support reps. Goal is to book a demo call.
> Output as CSV."

**Katelynn will:**
1. Clarify any missing ICP or value prop details
2. Search LinkedIn, Crunchbase, and job boards for matching companies
3. Find a specific research hook for each (e.g., "just posted 3 support roles on LinkedIn")
4. Draft a personalized cold email for each lead
5. Export everything to a clean CSV

---

## Output Format

### Leads Table (CSV)
```
number, name, title, company, website, linkedin, email,
research_hook, channel, subject_line, message, status, notes
```

### Message Draft (Markdown)
```
---
Lead #1: Jane Smith — Head of Customer Success at Acme Co
Channel: Email
Subject: Re: the 3 support roles at Acme

[Personalized message body]
---
```

---

## Using the Formatting Script

```bash
# Export to CSV
python scripts/format_output.py --leads leads.json --output my_leads.csv

# Export to Markdown
python scripts/format_output.py --leads leads.json --output my_leads.md --format md
```

**Input format** (`leads.json`):
```json
[
  {
    "name": "Jane Smith",
    "title": "Head of Customer Success",
    "company": "Acme Co",
    "website": "https://acmeco.com",
    "linkedin": "https://linkedin.com/in/janesmith",
    "email": "jane@acmeco.com",
    "research_hook": "Acme just posted 3 customer support roles on LinkedIn",
    "channel": "Email",
    "subject_line": "Re: the 3 support roles at Acme",
    "message": "Saw Acme is scaling the support team...",
    "status": "Draft ready"
  }
]
```

---

## Contributing

This skill is open source! Contributions welcome:
- Improved research strategies for niche industries
- New message frameworks
- Additional output formats (e.g., Google Sheets, Notion, HubSpot)
- Better eval cases

Please open a merge request on GitLab or file an issue.

---

## About gerika.ai

[gerika.ai](https://gerika.ai) is a hub for agentic AI agents you can hire for real tasks.
Katelynn is one of our flagship agents — this open-source skill is the same underlying
instruction set that powers her.

**More open-source skills:** [gitlab.com/gerika-ai/skills](https://gitlab.com/gerika-ai/skills)
**ClawHub listing:** [clawhub.ai/gerika-ai](https://clawhub.ai/gerika-ai)
