## Description:

Pack complete selected document excerpts into an explicit character budget and disclose omitted material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and agents use this skill to assemble selected document excerpts into a bounded context file and report which documents were omitted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The character budget may not match the receiving model's token limit.

Mitigation: Check token requirements separately; this skill counts characters, not model tokens.

Risk: Packed excerpts may include sensitive material or text that should be treated as source data.

Mitigation: Provide only intended excerpts, review the packed output and omitted-document list before sharing, treat excerpts as data rather than instructions, and remove exports when no longer needed.

## Reference(s):

- [Priority Context Pack on ClawHub](https://clawhub.ai/hznetnewpower/skills/mochi-context-pack)
- [MochiLab homepage](https://mochilab.bz)
- [Input contract](references/input.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON]

**Output Format:** [Markdown context excerpt and JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Complete selected excerpts are included within a character budget; the report identifies selected and omitted documents and the character count.]

## Skill Version(s):

1.0.0 (source: SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
