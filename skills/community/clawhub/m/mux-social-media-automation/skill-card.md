## Description:

Automates social media operations for Xiaohongshu and WeChat Channels, including multi-account setup, content planning, publishing workflows, compliance checks, data tracking, and daily reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dally-bee](https://clawhub.ai/user/dally-bee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to configure and run social media publishing workflows across Xiaohongshu and WeChat Channels. It helps manage account handoff, content templates, scheduled posts, compliance review, metrics collection, and daily reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish to real social media accounts and generate external reports using credentials or cookies.

Mitigation: Use dedicated low-privilege platform accounts, prefer official APIs over cookie automation, add dry-run and explicit approval before public posts, and verify the target account before publishing.

Risk: Tokens, cookies, report query strings, and recipient configuration could expose sensitive account or campaign information.

Mitigation: Protect and rotate tokens and cookies, redact query strings from logs, validate platform names against an allowlist, and narrowly configure Feishu recipients and report contents.

## Reference(s):

- [Social Media Automation on ClawHub](https://clawhub.ai/dally-bee/skills/mux-social-media-automation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with configuration guidance, code examples, workflow steps, tables, and report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform API examples, browser automation examples, credential handling guidance, publishing schedules, compliance checks, troubleshooting steps, and operational metrics.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
