## Description:

Skill dependency checker. Scan Python skills for external dependencies. Verify stdlib-only compliance, check individual files or entire skill directories. No database needed, pure file scanner.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexaiguy](https://clawhub.ai/user/nexaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan Python skill files or directories for imports classified as standard library, internal, or external before publishing or reviewing skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can miss dynamic or unusual imports and may report a project as clean when dependencies are present.

Mitigation: Use results as a lightweight local check only, then manually review suspicious code or confirm with a stronger parser-based scanner before publishing or approving a skill.

## Reference(s):

- [Nex DepCheck on ClawHub](https://clawhub.ai/nexaiguy/skills/nex-depcheck)
- [Nex AI](https://nex-ai.be)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with CLI commands and plain-text dependency scan results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports import classifications and clean/not-clean status for a file, one skill directory, or a directory of skills.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
