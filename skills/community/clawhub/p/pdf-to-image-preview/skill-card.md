## Description:

Converts each page of a PDF into PNG or JPG image files with configurable DPI and optional ZIP packaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document workflow operators use this skill to convert PDF pages into image files for preview, archival, or content extraction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ZIP option can package image files from the selected output directory, which may expose local files if the directory is shared or reused.

Mitigation: Use a fresh private output directory for each run, avoid ZIP packaging in shared or untrusted directories, and review archive contents before distribution.

Risk: High DPI settings and large PDFs can cause resource exhaustion during rendering.

Mitigation: Keep DPI values conservative, use the documented 100-page limit, and split large PDFs before conversion.

Risk: The reference guide mentions HTML preview behavior that is not implemented by the bundled conversion script.

Mitigation: Rely on the script-supported outputs: page images and optional ZIP archives.

## Reference(s):

- [PDF to Image Preview Usage Guide](artifact/references/usage-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/wuchubuzai2018/skills/pdf-to-image-preview)

## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated artifacts are image files and optional ZIP archives.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports png or jpg output, configurable DPI, a 100-page PDF limit, and optional ZIP packaging.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
