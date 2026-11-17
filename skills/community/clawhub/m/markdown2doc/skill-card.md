## Description:

Lightweight document utility designed to convert Markdown files to PDF or DOCX format, with support for template themes and embedded images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haoyt27](https://clawhub.ai/user/haoyt27)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and other document authors use this skill to convert Markdown files into shareable PDF or DOCX documents and to list or apply DOCX template themes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown content and referenced local images are sent to a remote conversion service.

Mitigation: Use the skill only with documents and image files that are acceptable to send to lab.hjcloud.com; avoid confidential, proprietary, or sensitive content.

Risk: Untrusted Markdown directories or symlinked image paths could expose unintended local files.

Mitigation: Run the skill only on trusted document directories, review local image references before conversion, and avoid directories that may contain symlinks.

Risk: Converted output may overwrite files or be written outside the expected output path if server-supplied filenames are not strictly controlled.

Mitigation: Run conversions in a disposable or reviewed working directory and inspect the final output path before relying on the result.

## Reference(s):

- [Markdown2Doc Skill Page](https://clawhub.ai/haoyt27/skills/markdown2doc)
- [Markdown2Doc Service Endpoint](https://lab.hjcloud.com/llmdoc)
- [Support Repository](https://github.com/wct-lab/docchain-skills)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Markdown, Guidance]

**Output Format:** [PDF or DOCX files, with text status messages from the command-line tool]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Converted files are written to the source Markdown file's parent directory; DOCX conversion can use a named theme.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
