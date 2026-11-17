## Description:

Tool-agnostic project collaboration for AI assistants that helps agents create project context, log activity, check shared state, query approved peer agents, and summarize cross-peer work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dp-pcs](https://clawhub.ai/user/dp-pcs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI assistant users use this skill to coordinate project work across collaborators while keeping each person's existing tools and local workflow. It guides agents to log project decisions and progress, check local project state, and query approved peer agents before starting related work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project intent and stored project details may be shared with approved peer agents.

Mitigation: Review peer approvals and response policies before enabling federation, and prefer escalate or summary modes for sensitive projects.

Risk: Sensitive project details, secrets, or private paths may be captured in project context.

Mitigation: Avoid entering secrets or private paths that should not be visible to collaborators or their agents.

Risk: The skill depends on a globally installed npm package and local OGP metadata storage.

Mitigation: Install only when comfortable with OGP storing project metadata, and consider pinning or isolating the npm package installation.

## Reference(s):

- [OGP documentation](https://github.com/dp-pcs/ogp)
- [ClawHub skill page](https://clawhub.ai/dp-pcs/skills/ogp-project)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the ogp CLI and local OGP state/configuration files.]

## Skill Version(s):

0.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
