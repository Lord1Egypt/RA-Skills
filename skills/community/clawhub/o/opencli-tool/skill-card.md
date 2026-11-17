## Description:

OpenCLI Tool Integration helps an agent use OpenCLI to retrieve website and social platform data, download media, control desktop applications, and pass commands to external CLI tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wike-chi](https://clawhub.ai/user/wike-chi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when they want an agent to collect data from supported websites, download media, interact with local desktop apps, or run registered CLI tools through OpenCLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad access to authenticated Chrome sessions, desktop applications, and powerful local CLIs.

Mitigation: Install only when that access is intended, prefer a separate Chrome profile and least-privileged accounts, and confirm write, message-sending, download, or administrative actions before allowing them.

Risk: Docker or Kubernetes access may expose sensitive local or cluster resources.

Mitigation: Enable Docker or Kubernetes commands only when needed and review the upstream OpenCLI package and browser extension before installation.

## Reference(s):

- [OpenCLI GitHub Repository](https://github.com/jackwener/opencli)
- [OpenCLI npm Package](https://www.npmjs.com/package/@jackwener/opencli)
- [ClawHub Skill Page](https://clawhub.ai/wike-chi/skills/opencli-tool)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured command output such as JSON, YAML, tables, CSV, or Markdown when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local commands that access authenticated browser sessions, desktop applications, downloaded files, and external CLI tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
