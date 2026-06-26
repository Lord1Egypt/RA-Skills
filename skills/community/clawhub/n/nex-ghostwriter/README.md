# Nex Ghostwriter

**Dump your meeting notes, get a follow-up email. One command, ready to send.**

Built by **Nex AI** - Digital transformation for Belgian SMEs.

## What It Does

- Log a meeting and generate a follow-up email in one step
- Five tone presets: professional, friendly, formal, casual, direct
- Regenerate the same meeting with a different tone
- Track which drafts you sent and which you skipped
- Store contacts with preferred greetings for personalized emails
- Generate both client follow-ups and internal team recaps
- Full-text search across all meetings
- Stats on meetings by type, client, and month
- Local SQLite storage. No telemetry. Your data stays on your machine.

## Quick Install

```bash
# Via ClawHub
clawhub install nex-ghostwriter

# Or manual
git clone https://github.com/Nex-AI-Guy/nex-ghostwriter.git
cd nex-ghostwriter
bash setup.sh
```

## Example Usage

**Client follow-up:**

```
User: Had a call with Marie from Lux Interiors. Premium plan, 2K budget, wants to start May.
      I need to send pricing and case studies.

Agent: I'll draft that follow-up.

> nex-ghostwriter draft "Premium plan - Lux Interiors" \
    --client "Marie Dubois" --email "marie@luxinteriors.be" \
    --notes "Discussed premium plan. Budget 2K/month. Start May." \
    --next-steps "Send pricing breakdown and case studies" \
    --tone professional

Subject: Follow-up: Premium plan - Lux Interiors - Marie Dubois

Hi Marie,

Thanks for the meeting earlier today. Here's a summary of what we discussed.

What we discussed:
   Discussed premium plan. Budget 2K/month. Start May.

Next steps:
   Send pricing breakdown and case studies

Let me know if anything needs adjusting.

Best regards,
```

**Different tone:**

```
> nex-ghostwriter redraft 1 --tone casual

Hey Marie,

Good chatting earlier today. Here's a quick recap of what we covered.
...
Cheers,
```

## Privacy

- All data stored locally at `~/.nex-ghostwriter/`
- No external API calls
- No telemetry, no analytics, no tracking
- You own your data

## CLI Reference

```
nex-ghostwriter draft        Log meeting + generate follow-up email
nex-ghostwriter redraft      Regenerate email with different tone
nex-ghostwriter show         Show meeting details + drafts
nex-ghostwriter view         View a draft's full email
nex-ghostwriter list         List meetings
nex-ghostwriter drafts       List all drafts
nex-ghostwriter sent         Mark draft as sent
nex-ghostwriter skip         Mark draft as skipped
nex-ghostwriter search       Search meetings
nex-ghostwriter edit         Edit meeting details
nex-ghostwriter contact-add  Add a contact
nex-ghostwriter contacts     List contacts
nex-ghostwriter stats        Show statistics
nex-ghostwriter export       Export to JSON or CSV
```

See SKILL.md for full command documentation.

## License

This project uses a dual license model:

**ClawHub (MIT-0):** Copies installed through ClawHub are licensed under MIT-0 as required by the platform. Free for any use.

**GitHub (AGPL-3.0):** Copies obtained from this GitHub repository are licensed under the GNU Affero General Public License v3.0. You may use, modify, and distribute freely, but if you offer a modified version as a service, you must open-source your changes.

**Commercial License:** Want to use this in a proprietary product or hosted service without AGPL obligations? Commercial licenses are available from Nex AI.

Contact: info@nex-ai.be | Website: [nex-ai.be](https://nex-ai.be)

---

Built by [Nex AI](https://nex-ai.be) -- Digital transformation for Belgian SMEs.

## Credits

- **Author**: Kevin Blancaflor
