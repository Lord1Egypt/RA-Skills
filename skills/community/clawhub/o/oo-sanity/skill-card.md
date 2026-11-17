## Description:

Operate Sanity through an OOMOL-connected account to read, query, create, update, and delete content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to retrieve and query Sanity documents or make content changes through a connected Sanity project. Confirm the exact payload and effect before write or destructive mutations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup runs a remote installer payload that remains unverified.

Mitigation: Review and approve CLI installation separately, preferably using a verified, fixed release.

Risk: CLI bundled-skill installation settings can affect installed agent skills.

Mitigation: Review those settings and, when appropriate, disable startup skill synchronization with OO_SKILLS_SYNC_DISABLED; connect only the Sanity access needed and retain approval checks for mutations.

## Reference(s):

- [Sanity HTTP API reference](https://www.sanity.io/docs/http-reference/query)
- [oo CLI command reference: environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Shell commands, JSON]

**Output Format:** [Markdown with oo CLI commands and JSON payloads or returned data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include Sanity data; mutations require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
