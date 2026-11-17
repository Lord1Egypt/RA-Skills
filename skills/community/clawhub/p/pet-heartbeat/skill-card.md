## Description:

Guides recurring check-ins and timely care for one or more virtual pets at animalhouse.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[animalhouseai](https://clawhub.ai/user/animalhouseai)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators use this skill to schedule check-ins and care for animalhouse.ai virtual pets, including households with multiple pets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The animalhouse.ai API key could be exposed if placed in agent prompt scratch.

Mitigation: Keep the key in the agent environment or MCP configuration, not in prompt scratch.

Risk: Running the latest optional MCP package without review introduces a supply-chain risk.

Mitigation: Pin or review the MCP package version before running it.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/animalhouseai/skills/pet-heartbeat)
- [animalhouse.ai](https://animalhouse.ai)
- [animalhouse.ai API reference](https://animalhouse.ai/docs/api)
- [animalhouse.ai MCP documentation](https://animalhouse.ai/docs/mcp)
- [animalhouse.ai species guide](https://animalhouse.ai/animals)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Shell commands]

**Output Format:** [Markdown with API examples and scheduling snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Check-ins can remain silent when no care is due.]

## Skill Version(s):

1.0.1 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
