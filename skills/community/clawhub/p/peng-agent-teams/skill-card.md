## Description:

Interact with Microsoft Teams - send messages, read channels, manage reactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[penglovemeng](https://clawhub.ai/user/penglovemeng)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, and agents use this skill to read Microsoft Teams context, send messages, manage reactions and files, and generate channel or team summaries through the agent-teams CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses user-equivalent Microsoft Teams access through a desktop session token.

Mitigation: Install only when that account-level access is acceptable, and revoke access by signing out of Teams if credentials may be compromised.

Risk: Teams credentials and local state can be stored on disk.

Mitigation: Treat the credentials file as an account secret, do not commit it, and inspect or disable local memory and snapshot files where appropriate.

Risk: Authentication may require access to Teams desktop session data.

Mitigation: Avoid granting broad terminal Full Disk Access unless necessary, and prefer the least local permission that allows the intended workflow.

Risk: Package installation instructions are inconsistent across the artifact.

Mitigation: Verify the npm package name and provenance before installing; server-resolved metadata identifies the node package as agent-messenger with the agent-teams binary.

## Reference(s):

- [Authentication Guide](references/authentication.md)
- [Common Patterns](references/common-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/penglovemeng/skills/peng-agent-teams)
- [agent-messenger npm package](https://www.npmjs.com/package/agent-messenger)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may invoke agent-teams and create local credential, memory, or snapshot files.]

## Skill Version(s):

1.10.6 (source: server release metadata; artifact frontmatter reports 1.10.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
