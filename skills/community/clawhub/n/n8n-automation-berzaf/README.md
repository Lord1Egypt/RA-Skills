# ⚡ n8n Automation Skill for OpenClaw

**Author:** berzaf | Berzaf AI Automation  
**Version:** 1.0.0  
**Category:** Automation / Productivity / Business  
**ClawHub slug:** `n8n-automation-berzaf`

---

## What This Skill Does

Bridges OpenClaw with n8n — the most powerful open-source
automation platform. Instead of manually triggering workflows,
you just talk to your agent in plain language and it fires
the right n8n webhook automatically.

**Built by an n8n expert** with years of integration experience.
Every workflow in this skill has been battle-tested in real
client deployments.

---

## 8 Included Workflows

| # | Workflow | Best For |
|---|----------|----------|
| 1 | Lead Nurture Email Sequence | Agencies, coaches, SaaS |
| 2 | Social Media Auto-Post | Content creators, founders |
| 3 | Meeting Follow-Up | Consultants, agencies |
| 4 | CRM Contact Update | Sales teams, freelancers |
| 5 | Competitor Monitor Report | E-commerce, SaaS |
| 6 | Invoice Reminder | Freelancers, agencies |
| 7 | Content Repurpose (YouTube/Blog) | YouTubers, bloggers |
| 8 | Daily Business Briefing | Solo founders, operators |

---

## Requirements

- A running n8n instance (self-hosted or n8n Cloud)
- Two environment variables:
  - `N8N_WEBHOOK_BASE_URL` — your n8n webhook base URL
  - `N8N_API_KEY` — your n8n API key for authentication

---

## Quick Install

```bash
clawhub install n8n-automation-berzaf
```

Then set your environment variables and restart your gateway:

```bash
export N8N_WEBHOOK_BASE_URL="https://your-n8n.com/webhook"
export N8N_API_KEY="your-key-here"
openclaw gateway restart
```

Test it works:
```
n8n status
```

---

## Example Conversations

**Lead nurture:**
> You: "Add john@startup.com to lead nurture, he came from YouTube"
> Agent: "Triggering lead nurture for John at john@startup.com (source: YouTube). Confirm?"
> You: "Yes"
> Agent: "Done. Sequence queued. ID: seq_a1b2c3"

**Social post:**
> You: "Post to LinkedIn and X: Just hit 7K subscribers on YouTube!"
> Agent: "Posting to LinkedIn and X: 'Just hit 7K subscribers on YouTube!' — Confirm?"
> You: "Yes go"
> Agent: "Posted. LinkedIn ID: li_xxx, X ID: tw_yyy"

**Morning briefing:**
> You: "Morning briefing"
> Agent: returns your full daily digest from n8n

---

## n8n Workflow Templates

The `/references/n8n-workflow-templates.md` file in this skill
package contains ready-to-import JSON templates for all 8 workflows.
Import them into your n8n instance in under 5 minutes.

---

## Support & Channel

Built by **Berzaf** — automation consultant and creator of
the **Berzaf AI Automation** YouTube channel covering n8n
workflows, OpenClaw integrations, and AI automation tutorials.

For questions, customization, or enterprise builds:
- YouTube: Berzaf AI Automation
- Custom builds available — contact via YouTube community

---

## License

MIT-0 — Free to use, modify, and distribute. No attribution required.
