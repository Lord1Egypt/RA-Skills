## Description:

Search and read Apple device and operating system build data through AppleDB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and assistants use this skill to search Apple devices and firmware builds and retrieve specific AppleDB records through the OOMOL-connected oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, the setup instructions can run a remote installer without a separate approval step; the installer and CLI were not audited.

Mitigation: Review and approve CLI installation separately before allowing lookups, preferably using a verified release.

Risk: Requests may require an OOMOL account or credits.

Mitigation: Check OOMOL access and available credits if a lookup cannot run.

## Reference(s):

- [AppleDB](https://appledb.dev)
- [AppleDB API documentation](https://github.com/littlebyteorg/appledb)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Guidance]

**Output Format:** [AppleDB lookup results as JSON or text, with shell commands and Markdown guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lookup results depend on AppleDB availability and OOMOL account access.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
