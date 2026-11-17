## Description:

Pinterest Ads data analysis and reporting via pinterest-ads-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bin-huang](https://clawhub.ai/user/bin-huang)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and marketing analysts use this skill to query Pinterest Ads account structure, campaign performance, audiences, billing, catalogs, trends, and analytics through a read-only CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install an unpinned third-party CLI globally.

Mitigation: Review before installing, prefer a pinned local install, and verify the npm package provenance before use.

Risk: Pinterest OAuth access may expose broad account, catalog, trend, billing, and ads-read permissions.

Mitigation: Use the narrowest OAuth scopes needed for the task and avoid sharing or logging access tokens.

Risk: Audience, billing, customer-list, and lead-form outputs can contain sensitive business or personal data.

Mitigation: Summarize or redact sensitive records unless the user clearly needs raw fields for the requested analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bin-huang/skills/pinterest-ads-cli)
- [Pinterest API v5 overview](https://developers.pinterest.com/docs/api/v5/)
- [Pinterest OAuth authentication](https://developers.pinterest.com/docs/getting-started/authentication/)
- [Pinterest Analytics API](https://developers.pinterest.com/docs/api/v5/#tag/ad_accounts)
- [Pinterest Catalogs API](https://developers.pinterest.com/docs/api/v5/#tag/catalogs)
- [Pinterest Trends API](https://developers.pinterest.com/docs/api/v5/#tag/trends)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides read-only Pinterest Ads CLI usage and may summarize sensitive account, billing, audience, customer-list, and lead-form data.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
