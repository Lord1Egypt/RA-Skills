## Description:

Use the OOMOL-connected ConvertAPI service to convert publicly accessible PDF files to DOCX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use this skill to convert a publicly accessible PDF to DOCX through an OOMOL-connected ConvertAPI account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial CLI setup runs an unverified remote installer, and the CLI may make broader changes than this skill describes.

Mitigation: Review and install the CLI separately, including its automatic agent-skill synchronization settings, before enabling the skill.

Risk: PDF conversion uses OOMOL and ConvertAPI and may incur service charges.

Mitigation: Use a PDF approved for processing through those services and check applicable charges before conversion.

## Reference(s):

- [ConvertAPI documentation](https://www.convertapi.com/docs/getting-started)
- [ConvertAPI homepage](https://www.convertapi.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell commands and JSON connector responses, including temporary DOCX download URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an external conversion service; returned download URLs are temporary.]

## Skill Version(s):

1.0.5 (source: artifact frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
