## Description:

P-E extracts structured data from a template image and multiple matching images, then generates an Excel workbook with the extracted rows and embedded source images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiou-max](https://clawhub.ai/user/haiou-max)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn similarly formatted product or record images into a formatted Excel spreadsheet. It is suited for batch image-to-table extraction where each row should include structured fields and an embedded source image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install unpinned Python packages from pip when dependencies are missing.

Mitigation: Review the dependency installation step before use and install approved versions of openpyxl and Pillow in a controlled environment when required.

Risk: The skill processes local images and may leave uploaded images in the predictable /tmp/p-e-images directory.

Mitigation: Use non-sensitive images when possible, clean /tmp/p-e-images after generating the spreadsheet, and verify the generated workbook before sharing it.

Risk: The generated spreadsheet may contain extraction errors from unclear or incomplete images.

Mitigation: Review cells marked [待确认], blank fields, and embedded images before using or distributing the Excel output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haiou-max/skills/p-e)
- [Publisher profile](https://clawhub.ai/user/haiou-max)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown status summary plus JSON data preparation, shell commands, and generated Excel files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates an .xlsx workbook with formatted headers, fixed column widths, embedded images, and row and column counts in the final report.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
