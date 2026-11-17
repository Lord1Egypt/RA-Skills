## Description:

Compresses verbose responses by removing filler and framing to save 200-400 tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to make verbose responses more concise while retaining useful information. It is intended for routine answers where brevity helps; the skill advises keeping detail for educational explanations and step-by-step setup instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compression can make an uncertain explanation sound definite and overstate confidence.

Mitigation: Keep uncertainty and confidence markers from the original response when shortening it; review compressed wording for changes in certainty.

## Reference(s):

- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve)
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-conserve-response-compression)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Concise natural-language responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Removes filler and framing while preserving clarity and necessary context.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
