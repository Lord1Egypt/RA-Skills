## Description:

Track Kenyan prepaid electricity (KPLC) tokens, predict blackout times, and get proactive low-balance alerts through chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lewisawe](https://clawhub.ai/user/lewisawe)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to manage Kenyan prepaid electricity by recording KPLC token SMS messages and meter readings, estimating remaining runtime, monitoring spending, and receiving low-balance or planned-outage alerts.

### Deployment Geography for Use:

Kenya

## Known Risks and Mitigations:

Risk: The skill can retain detailed household electricity records, full token values, and raw forwarded SMS text locally.

Mitigation: Use a restricted local account, keep the local database protected, and avoid forwarding unnecessary personal information.

Risk: Outage, reminder, calendar, or payment integrations can create side effects beyond a plain chat response.

Mitigation: Enable only the integrations you want and require confirmation before creating calendar events, reminders, or payment actions.

Risk: The planned-outage feature fetches and parses KPLC outage data from the public KPLC site.

Mitigation: Deploy only where outbound HTTPS access to KPLC is acceptable and review behavior before using it with real household data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lewisawe/skills/kplc-sentinel)
- [Publisher profile](https://clawhub.ai/user/lewisawe)
- [KPLC planned outage schedule PDF](https://www.kplc.co.ke/storage/01KPWN6FYWZ5Q9MKXJDHW7EG1A.pdf)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured JSON for the agent, followed by concise conversational text or Markdown for the user.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May support reminders, calendar events, and payment prompts through other installed skills when outages or low balances are detected.]

## Skill Version(s):

1.7.3 (source: server release metadata; artifact frontmatter says 1.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
