## Description:

Converts Markdown articles into themed HTML and helps publish complete WeChat draft posts through the mpa CLI, including embedded image handling and cover support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shijianzhong](https://clawhub.ai/user/shijianzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and developers use this skill to format Markdown articles with reusable themes and prepare or publish WeChat Official Account draft posts through the mpa command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dependency installation path asks users to execute mutable remote shell code.

Mitigation: Review the installer before use and prefer a pinned release, checksum-verified download, or package-manager installation for mpa.

Risk: Publishing can upload Markdown content, embedded images, cover images, and configured WeChat credentials to an external platform.

Mitigation: Confirm the intended Markdown file, media assets, cover image, destination account, and credentials before publishing.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/shijianzhong/skills/multi-platform-articles)
- [mpa installer script](https://raw.githubusercontent.com/shijianzhong/multi-platform-articles/main/scripts/install.sh)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration guidance, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated HTML output paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local HTML files and send article content, embedded images, cover images, and draft metadata to the configured WeChat account through mpa.]

## Skill Version(s):

0.1.18 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
