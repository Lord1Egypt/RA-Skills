## Description:

Use the OOMOL-connected Honeycomb account to inspect datasets, boards, markers, validate access, and create markers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People working with Honeycomb use this skill to inspect datasets and boards, validate account access, review markers, and create markers through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions run a downloaded CLI installer whose integrity and additional installation behavior have not been verified.

Mitigation: Review and approve CLI installation separately, prefer a verified release, and check what the installer adds before running it.

Risk: Honeycomb requests and results pass through OOMOL, and the connected account uses an API key.

Mitigation: Connect a suitably restricted API key and avoid granting broader access than the requested Honeycomb actions need.

## Reference(s):

- [Honeycomb](https://www.honeycomb.io/)
- [Honeycomb API documentation](https://docs.honeycomb.io/api/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [JSON requests and results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Marker creation changes Honeycomb data and requires confirmation of the exact action and payload.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
