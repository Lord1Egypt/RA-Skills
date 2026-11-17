## Description:

Gmail: Watch for new emails and stream them as NDJSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to have an agent guide Gmail watch sessions with the gws CLI, including Pub/Sub setup choices, label filters, polling, cleanup, and optional local JSON message output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can involve sensitive Gmail content and GCP Pub/Sub access.

Mitigation: Install and use it only when the gws CLI is authorized for the intended mailbox and GCP project.

Risk: The --output-dir option can store email contents locally.

Mitigation: Use a controlled output directory and handle generated JSON files according to the applicable data retention and access rules.

Risk: The --cleanup option removes watch-session Pub/Sub resources on exit.

Mitigation: Use --cleanup only when the created Pub/Sub resources should be deleted after the watch session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-gmail-watch)
- [gws-shared](../gws-shared/SKILL.md)
- [gws-gmail](../gws-gmail/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, flag descriptions, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe Gmail and GCP Pub/Sub command options, including local JSON output paths and cleanup behavior.]

## Skill Version(s):

1.0.12 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
