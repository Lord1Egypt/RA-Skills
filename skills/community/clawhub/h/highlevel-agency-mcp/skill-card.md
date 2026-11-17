## Description:

Preview HighLevel page and workflow changes, save domain bindings, and inspect settings for a connected sub-account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mooshee](https://clawhub.ai/user/mooshee)

### License/Terms of Use:

MIT-0

## Use Case:

HighLevel account administrators and agency teams use this skill to inspect a connected sub-account, audit settings and assets, and prepare supported page, workflow, and domain changes. It returns evidence and previews so users can review proposed changes before authorizing them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials entered for the hosted connection are sent to the Moosh Works service; renewable editing session credentials carry the HighLevel user's permissions and are not limited by the integration token's scopes.

Mitigation: Leave editing credentials empty for audits. For changes, use a dedicated user restricted to the intended sub-account and tasks, review each preview, and authorize changes separately.

Risk: Disconnecting the app does not rotate the underlying Private Integration Token or invalidate the original HighLevel editing session.

Mitigation: Rotate or delete the Private Integration Token in HighLevel, and ask an administrator or support to invalidate any editing session; confirm invalidation separately.

## Reference(s):

- [HighLevel Agency & Builder setup guide](https://ghlagencymcp.com)
- [HighLevel Private Integrations guidance](https://help.gohighlevel.com/support/solutions/articles/155000003054-private-integrations-everything-you-need-to-know)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Concise text summaries with structured tool-result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Account checks, audit findings, previews, and verification summaries; supported changes require a separate authorization step.]

## Skill Version(s):

1.1.4 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
