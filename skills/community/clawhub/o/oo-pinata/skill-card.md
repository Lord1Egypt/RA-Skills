## Description:

Use Pinata through an OOMOL-connected account to manage IPFS files, groups, and pin requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to read and manage Pinata files and groups, submit CID pin requests, and inspect pin request status through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pinning content changes storage state, and the skill's approval rules may not adequately identify that effect.

Mitigation: Before pinning, confirm the CID, destination account, and storage effect with the user.

Risk: The setup runs a remote installer, and the installer's behavior and hosted connector behavior were not verified.

Mitigation: Install the CLI through a separately reviewed, verified process and check its documented changes to other agent skills.

Risk: Connecting Pinata entrusts OOMOL with access to the connected account.

Mitigation: Connect an account whose access is appropriate for the requested Pinata actions.

## Reference(s):

- [Pinata](https://pinata.cloud)
- [Pinata API documentation](https://docs.pinata.cloud/api-reference/introduction)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell command instructions with JSON inputs and structured connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read data or change Pinata state; write and destructive actions are identified in the skill.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
