## Description:

PMO is an AI-native project-management office skill for OpenClaw that connects to project tools, summarizes status, sends alerts, and surfaces cross-project risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guytogay](https://clawhub.ai/user/guytogay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project managers, and delivery teams use this skill to query portfolio status, generate weekly reports, run risk checks, and track project intake across configured project-management sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read connected project-management data and retain local project and risk summaries.

Mitigation: Install only where that access is acceptable, prefer fine-grained read-only tokens, and review retained project, event, risk, and cache files.

Risk: The skill may send reports or alerts to configured external channels.

Mitigation: Disable or review automatic channel sending and confirm alert channels in configuration before use.

Risk: The GitHub integration requires an access token.

Mitigation: Provide tokens through environment variables such as GH_TOKEN and use a fine-grained read-only token.

## Reference(s):

- [PMO ClawHub listing](https://clawhub.ai/guytogay/skills/pmo)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown status reports and summaries, with JSON from integration scripts when fetching GitHub issue data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read configured project-management sources and write local project, event, risk, and cache files for PMO workflows.]

## Skill Version(s):

2.2.1 (source: server release metadata; artifact frontmatter is 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
