## Description:

AI project management assistant for planning, tracking, and managing projects using industry-standard methodologies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberneticsplus](https://clawhub.ai/user/cyberneticsplus)

### License/Terms of Use:

MIT

## Use Case:

Employees, external users, and developers use this skill to plan and track projects, manage risks, calculate earned value, run agile ceremonies, create WBS and Gantt artifacts, assign RACI responsibilities, and produce status reports for predictive, adaptive, or hybrid projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented runtime and installation paths can execute mutable remote npm or GitHub code with user-level access.

Mitigation: Review before installing, prefer a pinned and reviewed release or local audited executable, and use npm ci from a verified commit when building locally.

Risk: CLI commands can read user-provided files or project directories during risk scoring and health checks.

Mitigation: Run the CLI only against intended project files and directories, and avoid sensitive paths unless the executable has been reviewed.

## Reference(s):

- [PMP-Agentclaw ClawHub Skill Page](https://clawhub.ai/cyberneticsplus/skills/pmp-agentclaw)
- [CyberneticsPlus ClawHub Publisher Profile](https://clawhub.ai/user/cyberneticsplus)
- [README](artifact/README.md)
- [Disclaimer](artifact/DISCLAIMER.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON with optional shell commands and project document templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI tools can emit JSON or Markdown for earned value, risk scoring, velocity forecasting, and project health checks.]

## Skill Version(s):

1.0.3 (source: package.json, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
