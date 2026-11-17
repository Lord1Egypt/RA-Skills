## Description:

Use OKSign through an OOMOL-connected account to search and read account, user, and signed-document data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to retrieve OKSign credits, document metadata and links, active documents, and configured account users through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs users to run an unverified remote CLI installer; the installer and live connector code were not audited.

Mitigation: Review setup first, install a verified CLI version under your control, review or disable automatic skill synchronization, and limit use to the listed OKSign reads.

## Reference(s):

- [OKSign website](https://www.oksign.be/en/)
- [OKSign API documentation](https://www.oksign.be/public/api/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with shell command examples and JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands retrieve OKSign data through the connected account.]

## Skill Version(s):

1.0.5 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
