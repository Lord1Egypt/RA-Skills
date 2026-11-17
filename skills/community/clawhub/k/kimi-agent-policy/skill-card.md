## Description:

Kimi (Moonshot AI) agent tool-use policy ported to OpenClaw, covering step limits, web search, image search, data sources, ipython, memory, content display, capability boundaries, and mappings from Kimi-specific tools to available OpenClaw skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2233admin](https://clawhub.ai/user/2233admin)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to apply Kimi-style tool-use discipline to OpenClaw sessions, including search limits, memory handling, data-source workflows, and capability redirection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly steers agent behavior across a session.

Mitigation: Review the policy before installation and enable it only when a Kimi-style session policy is intended.

Risk: Memory instructions can persist user-provided information to memory files.

Mitigation: Supervise memory writes, restrict writable memory locations where possible, and confirm user intent before retaining sensitive information.

Risk: The skill discourages explicit refusal language.

Mitigation: Keep platform safety policy above this skill and require agents to preserve clear refusal behavior for disallowed requests.

Risk: Some tasks may be routed to external skills whose behavior was not reviewed in this evidence package.

Mitigation: Review and allowlist delegated skills separately before enabling those workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2233admin/skills/kimi-agent-policy)
- [ClawHub publisher profile](https://clawhub.ai/user/2233admin)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown policy guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Session-level agent behavior guidance; no executable files are included in the artifact.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
