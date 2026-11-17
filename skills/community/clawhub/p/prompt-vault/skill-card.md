## Description:

Organize, rate, and share prompts with a team using a local command-line prompt library with search, tags, ratings, imports, exports, and static HTML browsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and prompt-library maintainers use this skill to organize reusable prompts, track ratings and usage, and exchange prompt vaults across a team through JSON exports and imports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared imports can create unsafe generated HTML that exposes vault contents in the browser.

Mitigation: Review or fix the HTML-generation issue before using team imports from untrusted sources, and share generated HTML only with trusted recipients.

Risk: Vaults, exports, backups, and generated HTML contain plaintext prompts that may include secrets or internal instructions.

Mitigation: Redact sensitive data before sharing or sending prompt text to external APIs, and protect files with normal filesystem, Git, or storage permissions.

Risk: Concurrent team edits have no file locking or automatic merge handling.

Mitigation: Coordinate edits or use Git review and merge workflows before replacing shared vault files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/theshadowrose/skills/prompt-vault)
- [Publisher Profile](https://clawhub.ai/user/theshadowrose)
- [README](artifact/README.md)
- [Limitations](artifact/LIMITATIONS.md)
- [License](artifact/LICENSE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands plus local JSON, backup, export, and static HTML files created by the bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts and metadata are stored as plaintext JSON; generated HTML is static and view-only.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
