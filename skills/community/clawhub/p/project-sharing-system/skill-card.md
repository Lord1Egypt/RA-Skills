## Description:

Project Sharing System helps multiple agents share project status, discover active work, synchronize updates, keep history, and generate snapshots, summaries, backups, and an HTML dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep a shared project-status file, manage updates across multiple agents, and generate Markdown snapshots, summaries, backups, and a dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted workspace paths or project data could run code or browser script.

Mitigation: Install only in an isolated, trusted workspace and do not let untrusted users control CLAWHUB_WORKDIR or project data.

Risk: Dashboard rendering may expose users to browser script execution when served from a privileged or authenticated origin.

Mitigation: Avoid serving the dashboard from authenticated or privileged origins until the Python path handling and innerHTML rendering are fixed.

Risk: The security verdict is suspicious.

Mitigation: Review the skill before installing and scan it before deployment.

## Reference(s):

- [Project Sharing System on ClawHub](https://clawhub.ai/clementgu/skills/project-sharing-system)
- [clementgu ClawHub Publisher Profile](https://clawhub.ai/user/clementgu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation, JSON project status data, shell command output, and HTML dashboard files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Manages workspace files such as projects_status.json, PROJECT_STATUS.md, projects_snapshot.md, backups, and dashboard.html.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
