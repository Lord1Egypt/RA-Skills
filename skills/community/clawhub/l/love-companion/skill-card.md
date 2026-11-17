## Description:

Adds an adult-only AI companion roleplay mode with customizable personas, emotional dialogue, and persistent local memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moyan1638](https://clawhub.ai/user/moyan1638)

### License/Terms of Use:

MIT-0

## Use Case:

Adults use the skill with an AI agent for fictional romantic-companion conversations, persona customization, and locally retained relationship memories. It is not a replacement for human relationships or professional mental-health support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional trend awareness can carry untrusted web text into privileged agent instructions.

Mitigation: Leave trend awareness off unless the source pipeline is trusted; review external content before enabling it.

Risk: Locally stored relationship memories and profiles may contain sensitive personal information.

Mitigation: Limit what is shared, protect local storage, and export, delete, or purge retained data when no longer needed.

Risk: Romantic roleplay is intended for adults and should not substitute for human or professional support.

Mitigation: Require age confirmation before activation and retain clear AI-roleplay and support disclaimers.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/moyan1638/skills/love-companion)
- [Usage and commands](references/commands.md)
- [Persona presets](references/personas.md)
- [Architecture and data handling](docs/architecture.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Conversational text and JSON persona configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports persona presets, memory management, and optional trend-aware conversation.]

## Skill Version(s):

2.1.0 (source: server-resolved release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
