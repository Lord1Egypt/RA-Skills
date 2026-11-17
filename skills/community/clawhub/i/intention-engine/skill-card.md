## Description:

Intent inference and alignment for persistent AI agents: classifies gaps between tasks and intentions, checks for misalignment before executing, and prevents wasted work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mouserider](https://clawhub.ai/user/mouserider)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to help persistent AI agents infer user intent from profile goals, recent memory, project state, and active conversation context before choosing how to execute a request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages agents to infer intent from persistent context, which can misalign with the user's current request or privacy expectations.

Mitigation: Require explicit confirmation before irreversible, external-facing, costly, or privacy-impacting actions, and re-check inferred intent against current user context.

## Reference(s):

- [Nate Skelton's Intent Engineering](https://natesnewsletter.substack.com/)
- [Intention Engine on ClawHub](https://clawhub.ai/mouserider/skills/intention-engine)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown instructions for agent behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only skill; no API calls, tools, credential variables, or MCP references were detected.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
