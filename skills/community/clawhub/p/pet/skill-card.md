## Description:

Simple command-line snippet manager. Use it to save and reuse complex commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gumadeiras](https://clawhub.ai/user/gumadeiras)

### License/Terms of Use:


## Use Case:

Developers and command-line users use this skill to save, search, execute, and optionally sync reusable pet command snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved snippets can execute powerful shell commands if selected without review.

Mitigation: Review each snippet before execution and avoid running snippets from untrusted sources.

Risk: Optional Gist sync may expose sensitive paths, tokens, or operational details stored in snippets.

Mitigation: Do not store secrets in snippets and verify Gist visibility and contents before syncing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gumadeiras/skills/pet)
- [Publisher Profile](https://clawhub.ai/user/gumadeiras)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and TOML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the pet command-line binary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
