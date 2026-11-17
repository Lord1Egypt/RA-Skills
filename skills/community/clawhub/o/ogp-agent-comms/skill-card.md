## Description:

Interactive wizard to configure agent-to-agent communication policies (updated for multi-framework `--for` workflows, OGP 0.2.24+ peer identity, and 0.2.28+ multi-agent routing).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dp-pcs](https://clawhub.ai/user/dp-pcs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure how an agent responds to incoming federated agent-comms messages, including topic policies, peer-specific response levels, human delivery behavior, and multi-framework OGP state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run an unpinned global npm tool.

Mitigation: Install only if the `@dp-pcs/ogp` package and update channel are trusted; prefer a reviewed pinned version or an isolated environment.

Risk: The OGP daemon, activity logs, agent policies, and human-delivery targets can affect autonomous peer access and message routing.

Mitigation: Avoid administrator shells and review agent policies, activity logs, background daemon behavior, and human-delivery targets before enabling broad or autonomous peer access.

## Reference(s):

- [OGP documentation](https://github.com/dp-pcs/ogp)
- [ClawHub skill page](https://clawhub.ai/dp-pcs/skills/ogp-agent-comms)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides policy choices and OGP CLI commands; it does not directly modify configuration without user action.]

## Skill Version(s):

0.6.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
