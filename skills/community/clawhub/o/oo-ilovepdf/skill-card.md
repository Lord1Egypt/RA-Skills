## Description:

iLovePDF (ilovepdf.com). Use this skill for ANY iLovePDF request — searching and reading data. Whenever a task involves iLovePDF, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can operate iLovePDF through their connected OOMOL account to convert, merge, split, compress, protect, unlock, validate, or extract content from PDFs and related documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill directs users to run an unverified remote CLI installer; the installer and live connector code were not audited.

Mitigation: Install the oo CLI from a source you verify, review its automatic skill changes, and use OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization if needed.

Risk: The security review says document and password changes are incorrectly presented as safe reads.

Mitigation: Authorize each PDF transformation and password change explicitly, and provide only documents and PDF passwords you approve for processing through OOMOL/iLovePDF.

## Reference(s):

- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [iLovePDF](https://www.ilovepdf.com/)
- [iLoveAPI documentation](https://www.iloveapi.com/docs/api-reference)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Text]

**Output Format:** [Markdown guidance with shell command and JSON payload examples; actions may return processed PDFs, images, ZIP files, or extracted text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected PDF action and the files and options supplied.]

## Skill Version(s):

1.0.1 (source: release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
