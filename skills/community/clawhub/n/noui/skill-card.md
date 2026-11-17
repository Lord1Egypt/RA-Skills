## Description:

NoUI helps agents install and start using NoUI skills that record browser workflows and export them as FastMCP servers or Claude Code Skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gabriel-adopt](https://clawhub.ai/user/gabriel-adopt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use NoUI to discover and install the NoUI workflow skills, then set up browser workflow recording and export paths for MCP servers or Claude Code Skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install commands fetch mutable remote components that may change after review.

Mitigation: Pin the skills package version and the NoUI repository commit or signed release before installation.

Risk: Downstream NoUI components can operate with authenticated browser sessions, cookies, MCP servers, and agent skill directories.

Mitigation: Run setup in a least-privilege or disposable environment and review generated tools before granting access to sensitive sessions or directories.

Risk: The interactive bulk installer can block an agent on stdin.

Mitigation: Use the per-skill install commands with explicit --skill names when an agent performs installation.

## Reference(s):

- [NoUI ClawHub skill page](https://clawhub.ai/gabriel-adopt/skills/noui)
- [NoUI upstream repository referenced by artifact install commands](https://github.com/adoptai/noui)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown]

**Output Format:** [Markdown with bash command blocks and a skill-selection table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends per-skill install commands and warns agents not to use the interactive selector.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
