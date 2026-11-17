## Description:

Use Gainsight NXT to query, create, update, and delete company records through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and customer success teams use this skill to manage Gainsight NXT company records through a connected account, including queries and approved record changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute changing remote code and may install other agent skills without separate approval.

Mitigation: Verify a specific oo CLI release and review or disable automatic skill installation before setup.

Risk: Write and deletion actions can change Gainsight customer records.

Mitigation: Use a suitably restricted Gainsight account and require approval for every write or deletion.

## Reference(s):

- [Gainsight NXT API documentation](https://support.gainsight.com/gainsight_nxt/API_and_Developer_Docs/About/API_Documentation_Overview)
- [Gainsight](https://www.gainsight.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Guidance]

**Output Format:** [Natural-language responses and JSON connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned fields and result structure depend on the selected action and Gainsight tenant schema.]

## Skill Version(s):

1.0.5 (source: skill frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
