## Description:

Embase (elsevier.com). Use this skill for ANY Embase request — searching and reading data. Whenever a task involves Embase, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and other users can search biomedical literature in Embase and retrieve individual article records through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute an unverified remote installer without a clear approval step, and the installer's effects and exact downloaded release are unverified.

Mitigation: Review and approve CLI installation separately, verify the release, and check its automatic agent-skill synchronization settings.

Risk: Embase queries use the user's OOMOL-connected account.

Mitigation: Confirm the connected account and its intended Embase access before querying.

## Reference(s):

- [Embase product information](https://www.elsevier.com/products/embase)
- [Embase API documentation](https://dev.elsevier.com/embase_apis.html)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON article records and concise agent-readable text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action and access available to the connected Embase account.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
