## Description:

Use the OOMOL-connected Omnisend account to read, create, update, and delete contact and segment data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Omnisend contacts and segments through their OOMOL-connected account, including reading data and making confirmed changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup can execute unverified remote installer code without a separate approval step; the remote installers and hosted connector are not fully verified.

Mitigation: Review and approve CLI installation separately, using a verified release where possible, and check automatic skill installation and synchronization settings before running it.

Risk: Connecting Omnisend entrusts OOMOL with account access and contact operations.

Mitigation: Keep permissions narrow and retain the documented confirmations before write or destructive actions.

## Reference(s):

- [Omnisend API documentation](https://api-docs.omnisend.com/reference/overview)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Omnisend skill release](https://clawhub.ai/oomol/skills/oo-omnisend)

## Skill Output:

**Output Type(s):** [JSON data, Text summaries]

**Output Format:** [JSON responses with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contact and segment data returned by Omnisend; write and destructive actions require confirmation as specified by the skill.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
