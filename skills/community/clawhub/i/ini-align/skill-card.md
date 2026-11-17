## Description:

INI file section and key-value alignment tool that reorders sections and keys in a target INI file to match a source reference file while preserving target-only content and listing source-only sections as comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imvvip](https://clawhub.ai/user/imvvip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to align INI configuration files against a reference order before reviewing or applying configuration updates. It is useful when section order and key order need to be normalized while keeping target-only settings visible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The output path can overwrite source, target, or other writable files if it is unsafe.

Mitigation: Use explicit source, target, and fresh output paths, avoid aliases to input files, and keep backups for important configuration files until output path handling rejects existing files.

## Reference(s):

- [Ini Align ClawHub Skill Page](https://clawhub.ai/imvvip/skills/ini-align)
- [imvvip ClawHub Publisher Profile](https://clawhub.ai/user/imvvip)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and generated INI file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script writes an aligned INI output file and prints a markdown-style statistics table with duplicate-section warnings when present.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
