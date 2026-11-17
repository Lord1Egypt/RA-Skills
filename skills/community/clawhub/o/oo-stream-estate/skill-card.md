## Description:

Search and read Stream Estate property data through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Stream Estate can search locations and property listings, retrieve a property record, or find similar properties through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup directs the agent to execute a remote installer payload that the security review could not verify.

Mitigation: Install and verify the CLI yourself, inspect its bundled-skill installation and update behavior, and explicitly approve local changes.

Risk: Use depends on an OOMOL-connected account and may require credit.

Mitigation: Confirm the required account connection and any applicable credit requirements before use.

## Reference(s):

- [Stream Estate](https://stream.estate)
- [Stream Estate API documentation](https://docs.stream.estate/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Property data returned as JSON, with concise text summaries and shell commands for queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Stream Estate account and available service access.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
