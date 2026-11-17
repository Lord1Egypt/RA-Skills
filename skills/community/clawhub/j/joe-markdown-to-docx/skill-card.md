## Description:

Convert Markdown files to fully formatted Word DOCX documents with support for tables, images, code blocks, and GitHub Flavored Markdown features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joecao](https://clawhub.ai/user/joecao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document authors use this skill to convert Markdown source files into editable Word DOCX documents while preserving common formatting, tables, images, links, and code blocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown image references can trigger outbound network requests when remote image URLs are processed.

Mitigation: Run the skill on trusted Markdown only, or execute it in a sandbox with limited outbound network access and block private or internal network targets.

Risk: Local image references can read files outside the Markdown document directory after path resolution.

Mitigation: Constrain local image paths to the Markdown document directory before use and review documents from other people before conversion.

Risk: Large or hostile Markdown, images, or data URLs can consume excessive processing time or memory.

Mitigation: Apply file size, image size, and execution time limits when converting untrusted or externally supplied input.

Risk: The Node dependency tree is installed from a third-party registry mirror.

Mitigation: Prefer reproducible installation with npm ci and review the registry source and locked dependency versions before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/joecao/skills/joe-markdown-to-docx)
- [Publisher Profile](https://clawhub.ai/user/joecao)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [DOCX file output with Markdown and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Converts a single Markdown input path to a DOCX output path; remote, local, and data URL images may be embedded when available.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
