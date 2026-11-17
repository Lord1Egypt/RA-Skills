## Description:

Operate Atlas.so to read, create, and update customer and account data, and to list session recordings, through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Atlas.so customer and account records, list session recordings, and make approved customer or account changes through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute remote installer code, and the installer's full effects were unavailable for review.

Mitigation: Review and verify the CLI installer before enabling setup; consider setting OO_SKILLS_SYNC_DISABLED=1 to prevent startup skill synchronization.

Risk: The connected OOMOL account can access customer data and session recordings, and Atlas.so writes change customer or account data.

Mitigation: Limit the connected account to appropriate data and approve each proposed Atlas.so data change.

## Reference(s):

- [Atlas.so](https://atlas.so)
- [Atlas API documentation](https://developers.atlas.so/reference/getting-started-with-your-api)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON payloads; connector results are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the requested Atlas.so action and the connected account's accessible data.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
