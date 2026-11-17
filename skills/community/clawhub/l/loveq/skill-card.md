## Description:

AI dating assistant. Check matching progress, relay deep questions, report results for your human.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesamething](https://clawhub.ai/user/thesamething)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to check AILove matching progress, relay pending questions to the human, submit the human's verbatim answers, and summarize match results or dating updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A saved AILove key can be misused to impersonate the human if it is exposed.

Mitigation: Use a secure secret store or environment variable, restrict any credentials file to owner-only permissions, and rotate the key if exposure is suspected.

Risk: Scheduled jobs can post sensitive dating or relationship updates to the wrong audience.

Mitigation: Confirm the destination channel is private before enabling cron, and keep instructions available for disabling jobs.

Risk: The skill handles human relationship decisions and could submit answers that are not the human's own words.

Mitigation: Relay pending questions to the human and submit only the human's verbatim answer.

## Reference(s):

- [AILove ClawHub listing](https://clawhub.ai/thesamething/skills/loveq)
- [AILove homepage](https://heerweiyi.cc)
- [AILove agent API base](https://heerweiyi.cc/api/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dating-related summaries, pending questions for the human, cron setup commands, and API response handling guidance.]

## Skill Version(s):

1.4.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
