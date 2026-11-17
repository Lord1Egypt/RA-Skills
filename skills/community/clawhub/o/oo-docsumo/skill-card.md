## Description:

Docsumo (docsumo.com). Use this skill for ANY Docsumo request — reading, creating, and updating data. Whenever a task involves Docsumo, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People who manage Docsumo documents can use the skill to inspect account and document information, retrieve extracted data, and upload a document from a public URL. Uploading changes the connected Docsumo account and requires confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded software, and the downloaded installers and hosted implementation are unverified.

Mitigation: Review setup first, install a reviewed and version-pinned CLI yourself, and disable automatic skill synchronization if you want only this integration.

Risk: The connected Docsumo account may expose document data to the agent and OOMOL; uploads change account state.

Mitigation: Connect an account whose document data is intended for this use, and confirm each upload and its target before running it.

## Reference(s):

- [Docsumo](https://www.docsumo.com)
- [Docsumo API documentation](https://support.docsumo.com/reference/getting-started-with-your-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: skill frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
