## Description:

Verify code references against the repository before trusting them. Use when writing, renaming, or reviewing code, imports, paths, or comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gonisulaimann](https://clawhub.ai/user/gonisulaimann)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code-review agents use this skill to verify repository references before relying on imports, paths, symbols, comments, or documentation claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional setup or fix commands can write files, including global skill installation targets or non-dry-run rewrites.

Mitigation: Review init-agent commands before running them and prefer dry-run fix commands before allowing file changes.

## Reference(s):

- [Rules reference](references/rules.md)
- [Commands reference](references/commands.md)
- [Grounded rules documentation](https://grounded.readthedocs.io/en/latest/rules/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline console and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May advise dry-run checks before file-writing commands; scan, impact, MCP, and LSP workflows are documented as non-writing paths.]

## Skill Version(s):

0.16.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
