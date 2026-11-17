## Description:

Project Manager Pro lets an OpenClaw agent create, organize, prioritize, review, and export local JSON-backed tasks and projects through conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to turn plain-language requests into structured task lists, project plans, priority views, scheduled check-ins, and exports without opening a separate task-management app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can request administrator-level package installation when jq is missing.

Mitigation: Review setup.sh before running it and install jq manually through a trusted package manager when possible.

Risk: Task stores and exports may contain sensitive work, finance, health, schedule, or cross-tool context in plaintext.

Mitigation: Protect the pm-pro directory and exported files with local access controls, disk encryption, and careful sharing practices.

Risk: Task content is processed through the user's configured agent and LLM provider.

Mitigation: Review the LLM provider's data policy and avoid storing highly sensitive tasks unless the configured provider and channel visibility are acceptable.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nollio/skills/project-manager-pro)
- [Security considerations](artifact/SECURITY.md)
- [Dashboard specification](artifact/dashboard-kit/DASHBOARD-SPEC.md)
- [Configuration defaults](artifact/config/settings.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Conversational text and Markdown task views, local JSON task and project records, and optional Markdown, CSV, or JSON exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores task and project data locally under ~/.openclaw/workspace/pm-pro; exports are plaintext files.]

## Skill Version(s):

1.0.0 (source: server release evidence and config/settings.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
