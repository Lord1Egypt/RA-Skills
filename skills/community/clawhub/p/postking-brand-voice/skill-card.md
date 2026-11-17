## Description:

List and apply saved PostKing voice profiles when generating or rewriting content, and run a de-slop pass that strips LLM clichés and filler.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitsandtea](https://clawhub.ai/user/bitsandtea)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing teams use this skill to apply existing PostKing brand voice profiles to generated or rewritten content, then review the result for generic or templated phrasing before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rewritten content may still contain inaccurate, generic, or off-brand language.

Mitigation: Review the rewritten text before publishing and use the diagnostic check only to guide human revision.

Risk: Users may submit sensitive text to PostKing rewriting tools without confirming their setup is appropriate for that data.

Mitigation: Avoid submitting sensitive content unless the configured PostKing environment and account policies permit it.

Risk: The de-slop pass could be misused to hide AI authorship where disclosure is required.

Mitigation: Follow platform, client, publisher, and legal disclosure requirements for AI-assisted content.

## Reference(s):

- [PostKing MCP endpoint](https://mcp.postking.app/mcp)
- [ClawHub skill page](https://clawhub.ai/bitsandtea/skills/postking-brand-voice)
- [Skill icon](https://raw.githubusercontent.com/bitsandtea/postking-skills/main/assets/icons/postking-brand-voice.svg)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with optional inline tool calls and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces rewritten content, voice-profile identifiers, diagnostic quality checks, and concise next-step guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
