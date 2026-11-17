## Description:

Meta Ads data analysis and reporting via meta-ads-open-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bin-huang](https://clawhub.ai/user/bin-huang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and analytics teams use this skill to query Meta/Facebook/Instagram ad accounts, pull performance insights, inspect creatives and audiences, check pixel events, and retrieve lead form submissions through a read-only CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive Meta Ads account data and lead form submissions.

Mitigation: Use a dedicated Meta OAuth token with the minimum required permissions, retrieve lead data only when necessary, and redact personal data by default.

Risk: The artifact suggests a global unpinned npm install for the CLI package.

Mitigation: Install only if the package is trusted, and prefer a pinned version or locally isolated installation.

## Reference(s):

- [meta-ads-open-cli documentation](https://github.com/Bin-Huang/meta-ads-open-cli)
- [Meta Marketing API overview](https://developers.facebook.com/docs/marketing-apis/)
- [Ad Insights API](https://developers.facebook.com/docs/marketing-api/insights/)
- [Custom Audiences API](https://developers.facebook.com/docs/marketing-api/audiences/)
- [Lead Ads API](https://developers.facebook.com/docs/marketing-api/guides/lead-ads/)
- [Ad Creative reference](https://developers.facebook.com/docs/marketing-api/reference/ad-creative)
- [ClawHub skill page](https://clawhub.ai/bin-huang/skills/meta-ads-open-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI commands output pretty-printed JSON by default; compact JSON is available with --format compact.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
