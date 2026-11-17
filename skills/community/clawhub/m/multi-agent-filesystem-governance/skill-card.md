## Description:

Govern filesystem organization and file-operation decisions in multi-agent environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darinrowe](https://clawhub.ai/user/darinrowe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent operators use this skill to decide where files should live, how they should be scoped, and when file operations could affect shared or multi-agent workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence where agents create, move, or archive files, which may affect shared workspaces if applied too broadly.

Mitigation: Apply the skill's narrow-scope guidance: prefer agent-private locations, use non-destructive actions, and avoid shared writes unless reuse or collaboration is intentional.

Risk: Temporary or scratch locations can be mistaken for durable storage for important work.

Mitigation: Move or copy important artifacts into an active private, shared, project, or archive location once they need to persist.

## Reference(s):

- [Anti-Patterns](references/anti-patterns.md)
- [Examples](references/examples.md)
- [Project Directory Best Practices](references/project-directory-best-practices.md)
- [ClawHub Skill Page](https://clawhub.ai/darinrowe/skills/multi-agent-filesystem-governance)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration instructions]

**Output Format:** [Markdown guidance with scope, lifecycle, recommended location type, reason, and shared-impact note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, network access, credential handling, or hidden execution behavior identified in server security evidence.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
