## Description:

OpenClaw Skill Creator helps users generate custom OpenClaw skills from plain-English requests, including skill files, setup steps, testing prompts, and troubleshooting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kennyzir](https://clawhub.ai/user/kennyzir)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create OpenClaw skills for workflow-specific integrations, local file processing, and API-backed automations without writing the skill manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated skills may require sensitive credentials such as Google credential JSON files or Slack tokens.

Mitigation: Review generated skills before installing them, avoid pasting real secrets into SKILL.md, and store credentials outside published skill folders.

Risk: Generated skills may read sensitive calendars, files, or business data, or post messages to external collaboration services.

Mitigation: Require explicit approval before enabling those actions and use least-privilege service permissions.

Risk: Generated setup guidance may install dependencies that are not pinned.

Mitigation: Pin and review dependencies before installation, then scan generated skills before deployment.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/kennyzir/skills/openclaw-skill-creator-pro)
- [OpenClaw Skill Creator Documentation](https://claw0x.com/docs/openclaw-skill-creator)
- [Google Calendar API Node.js Quickstart](https://developers.google.com/calendar/api/quickstart/nodejs)
- [Slack API Quickstart](https://api.slack.com/start/quickstart)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON with embedded Markdown and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated skills may include dependency installation steps and environment-variable setup for external services.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
