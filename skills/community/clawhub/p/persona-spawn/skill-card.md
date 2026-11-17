## Description:

Spawn subagents with personas from a local workspace library or the Emblem persona marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[decentraliser](https://clawhub.ai/user/decentraliser)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to delegate bounded tasks to subagents with a selected persona, while keeping persona materials local or imported from a marketplace and preserving shared organization context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Imported marketplace persona files can influence spawned subagents.

Mitigation: Review imported personas before use and avoid bulk imports unless the source is trusted.

Risk: Shared context files can expose sensitive local information to a spawned subagent.

Mitigation: Keep context_files limited to non-secret documents and do not point them at credentials, private keys, agent state, or unrelated personal files.

Risk: The release security verdict is suspicious because the skill imports mutable remote prompt content and can include broad local files in subagent prompts.

Mitigation: Review the skill and its imported persona content before installing or running it.

## Reference(s):

- [ClawHub Persona Spawn listing](https://clawhub.ai/decentraliser/skills/persona-spawn)
- [Emblem Persona Marketplace API](references/api-endpoints.md)
- [Writing a Custom SOUL.md](references/soul-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persona setup guidance, deterministic subagent prompt assembly steps, and normal subagent task results.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
