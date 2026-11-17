## Description:

Advertises color-palette generation and management for UI and brand color systems, but server security review says the bundled script behaves mainly as a local log, search, and status utility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External designers and frontend developers may use the skill for palette-related command guidance and local palette records. Review the implementation before relying on it for actual palette generation or export workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertised palette generation and export behavior may not match the bundled implementation.

Mitigation: Review or correct the implementation before using it in design, brand, or customer-facing workflows.

Risk: The artifact can persist local command records under ~/.palette.

Mitigation: Do not pass secrets, private prompts, customer names, or sensitive brand material unless storage and export behavior is documented and acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ckchzh/skills/palette)
- [Publisher Profile](https://clawhub.ai/user/ckchzh)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and environment variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local files under ~/.palette when executed.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
