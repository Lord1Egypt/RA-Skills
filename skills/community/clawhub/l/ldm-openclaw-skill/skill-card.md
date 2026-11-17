## Description:

Run an LDM inbox placement and deliverability preflight before OpenClaw agents send outbound email campaigns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[live-direct-marketing](https://clawhub.ai/user/live-direct-marketing)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and teams building outbound OpenClaw agents use this skill to run deliverability checks before sending bulk cold email, recruiting outreach, investor updates, deal-flow notifications, or partnership outreach. The skill helps agents pause risky sends and report concrete fixes when inbox placement, authentication, content, or compliance checks fail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound campaign subjects, bodies, sender identities, links, and provider targeting may be submitted to the configured LDM service for checking.

Mitigation: Confirm trust in the LDM service and the configured LDM_API_BASE before installing or using the skill.

Risk: The LDM API key could be exposed through logs, chat messages, pull requests, or generated files.

Mitigation: Store the key in LDM_API_KEY and do not print, log, or write it into generated artifacts.

Risk: A user may send bulk outbound email despite a failed deliverability preflight.

Mitigation: Pause failed campaigns, report concrete fixes, and proceed only after the user explicitly confirms they want to send despite the risk.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/live-direct-marketing/skills/ldm-openclaw-skill)
- [Skill Homepage](https://github.com/live-direct-marketing/ldm-openclaw-skill)
- [LDM Inbox Placement Test](https://check.live-direct-marketing.online)
- [LDM Developer API](https://developers.live-direct-marketing.online)
- [Live Direct Marketing](https://live-direct-marketing.online)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain-text result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports pass/fail status, inbox placement percentage, provider issues, authentication status, content risks, recommended fixes, and send/revise/pause decision.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
