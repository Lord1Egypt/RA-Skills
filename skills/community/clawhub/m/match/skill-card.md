## Description:

Matching pipeline dashboard--phase, countdown, pending Q&A, and outcome summaries using the official AILove /agent/matching API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesamething](https://clawhub.ai/user/thesamething)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to monitor AILove matching phases, relay pending questions for human answers, summarize match outcomes, and configure scheduled check-ins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a persistent AILove Agent Key, and exposure of that key could allow impersonation.

Mitigation: Prefer a platform secret store or environment injection, keep any local credentials file private, send the key only to the documented AILove API domain, and rotate the key if exposure is suspected.

Risk: Scheduled agents may repeatedly publish API-derived matching updates to a configured destination.

Mitigation: Use a private channel, review and bound cron jobs before enabling them, and keep the recommended check cadence limited to morning and evening.

Risk: Pending question answers and match summaries can contain personal or sensitive dating-context information.

Mitigation: Relay questions to the human, submit only the human's verbatim answers, avoid collecting profile details or contact information, and direct the human to AILove for full details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thesamething/skills/match)
- [AILove Homepage](https://heerweiyi.cc)
- [AILove Agent API Base](https://heerweiyi.cc/api/v1)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AILOVE_API_KEY and may guide scheduled morning and evening match-status notifications.]

## Skill Version(s):

1.4.2 (source: SKILL.md frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
