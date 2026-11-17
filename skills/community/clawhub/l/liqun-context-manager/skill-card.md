## Description:

Manages conversation context and memory extraction by searching historical memory for keywords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaxint](https://clawhub.ai/user/jaxint)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to search local memory files by keyword and retrieve recent memory entries for conversation context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill searches installed skill files in addition to memory files, which is not disclosed in the user-facing instructions.

Mitigation: Restrict use to a dedicated memory directory or clearly document and gate any search outside memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaxint/skills/liqun-context-manager)
- [ClawHub publisher profile](https://clawhub.ai/user/jaxint)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Plain text paths, Python return values, and optional CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are limited by a count parameter, and recent memory retrieval returns filenames.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
