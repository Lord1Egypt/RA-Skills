## Description:

Render responses in a structured, modular UMG speech style with GPT-4o-inspired conversational polish for highly readable chat output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neomagnetar](https://clawhub.ai/user/neomagnetar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to reformat agent responses into clearer, sectioned, scan-friendly chat output without changing the underlying meaning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic requests such as 'format this' or 'clean this up' may trigger the modular speech style when the user did not intend a persistent style change.

Mitigation: Ask the agent to stop, return to normal tone, or switch styles when the formatting layer is no longer desired.

Risk: Direct slash alias support may vary across OpenClaw surfaces.

Mitigation: Use the documented '/skill poe-umg' invocation path when '/poe-umg' is not dispatched by the current surface.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neomagnetar/skills/poe-umgo-modular-speech)
- [Publisher profile](https://clawhub.ai/user/neomagnetar)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Formatting-only response transformation; no code execution, data access, networking, or privileged behavior is added.]

## Skill Version(s):

1.0.3 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
