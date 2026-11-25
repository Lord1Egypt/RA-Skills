## Description:

Create Arabic Word documents with right-to-left layout, suitable Arabic and Latin fonts, Arabic-Indic numerals, and verified formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alsoulm](https://clawhub.ai/user/alsoulm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and writers use this skill to create or repair Arabic Word documents with reliable right-to-left text, font pairing, numerals, tables, and table of contents formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The PDF-preview guide removes the shared /tmp/render directory, which may contain files from another run.

Mitigation: Use a unique temporary directory for each preview and limit cleanup to that directory after checking its path.

Risk: The security scan reports that part of the artifact was only partially inspected.

Mitigation: Review the partially inspected script before installing or running the skill.

## Reference(s):

- [Arabic DOCX Guide](references/arabic-docx-guide.md)
- [Global Proposal on ClawHub](https://clawhub.ai/alsoulm/skills/global-proposal)

## Skill Output:

**Output Type(s):** [Word documents, PDF previews, Code, Shell commands, Guidance]

**Output Format:** [Arabic .docx files with PDF previews, plus supporting JavaScript/Python code and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Right-to-left layout, Arabic and Latin font pairing, Arabic-Indic numerals, and document checks.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
