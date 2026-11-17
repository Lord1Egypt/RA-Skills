## Description:

Helps agents prepare, adapt, schedule, publish, and track book releases across Amazon KDP, Chinese fiction platforms, Royal Road, and related channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ouyang198000](https://clawhub.ai/user/ouyang198000)

### License/Terms of Use:

MIT-0

## Use Case:

External users and publishing operators use this skill to adapt manuscripts, covers, metadata, schedules, and status reporting for multi-platform book publication workflows. The skill also describes assisted account login, upload, review submission, scheduling, and publication status collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate account login, uploads, public posting, and publishing schedules across multiple platforms.

Mitigation: Require explicit user approval for each target platform, account, manuscript, upload, and publish or schedule action.

Risk: Third-party CAPTCHA solving may violate platform rules or expose verification data.

Mitigation: Disable automatic CAPTCHA solving unless the target platform permits it and the user accepts the privacy implications; prefer pausing for human verification.

Risk: Stored credentials, broad session access, and verbose logs can expose publishing accounts or manuscript details.

Mitigation: Avoid stored credentials where possible, limit session access to the immediate task, and return only the minimum publication status and exception details needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ouyang198000/skills/multi-platform-publisher-agent)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or JSON-style status reports with platform links, book IDs, review status, schedules, and exception notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform configuration examples, publishing workflow steps, generated book metadata, and cover handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
