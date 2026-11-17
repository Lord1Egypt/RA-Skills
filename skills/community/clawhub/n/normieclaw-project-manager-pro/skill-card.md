## Description:

Project Manager Pro helps an agent manage local tasks and projects through conversation, including task creation, prioritization, project breakdowns, status updates, exports, and check-ins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an OpenClaw agent maintain personal task and project records, break down goals, surface priorities, generate check-ins, and export task data from a local workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can make system-level package changes while installing jq.

Mitigation: Review setup.sh before installation and install jq manually if automatic package-manager or sudo changes are not acceptable.

Risk: Task, project, check-in, and export data are stored as plaintext local files.

Mitigation: Use disk encryption, apply local access controls, and handle Markdown, CSV, and JSON exports as sensitive files.

Risk: Task content may be processed by the configured LLM provider and may include context imported from other tools.

Mitigation: Review the provider data policy and disable cross-tool integrations when tasks may contain sensitive information.

Risk: Scheduled check-ins or task responses may expose task details in shared agent channels.

Mitigation: Configure the agent only in appropriate channels and review check-in settings, quiet hours, and channel visibility before enabling proactive use.

Risk: CSV exports can be risky when task text comes from untrusted sources and is opened in spreadsheet software.

Mitigation: Inspect or sanitize CSV exports before opening them in spreadsheet applications.

## Reference(s):

- [Project Manager Pro on ClawHub](https://clawhub.ai/nollio/skills/normieclaw-project-manager-pro)
- [Publisher profile](https://clawhub.ai/user/nollio)
- [README](artifact/README.md)
- [Security considerations](artifact/SECURITY.md)
- [Dashboard specification](artifact/dashboard-kit/DASHBOARD-SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV, shell commands, configuration, guidance]

**Output Format:** [Conversational text and Markdown summaries, with JSON task and project records plus Markdown, CSV, or JSON exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local plaintext files under the OpenClaw workspace; setup and export flows may involve shell scripts.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
