## Description:

Convert markdown files to properly formatted Google Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brennerspear](https://clawhub.ai/user/brennerspear)

### License/Terms of Use:


## Use Case:

Developers, researchers, and other document authors use this skill to convert local Markdown files into Google Docs while preserving common document formatting such as headings, bold text, code blocks, lists, links, blockquotes, and tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown file contents are uploaded to Google Docs and could be sent to the wrong Google account or Drive folder.

Mitigation: Before execution, verify the selected Markdown file, Google account, document title, and Drive folder.

Risk: Markdown without proper heading markers may convert with all content as body text.

Mitigation: Check that headings use # through ###### syntax before running the conversion.

## Reference(s):

- [gog Google Workspace CLI](https://github.com/tychohq/gog)
- [Md To Gdoc ClawHub Skill Page](https://clawhub.ai/brennerspear/skills/md-to-gdoc)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script outputs the created Google Doc URL on success.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
