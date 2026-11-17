## Description:

Meta Ad Spy helps agents research competitor advertising on Meta platforms by collecting public Meta Ad Library data, optionally querying the Meta Graph API, and synthesizing competitive intelligence reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhishekj9621](https://clawhub.ai/user/abhishekj9621)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, growth analysts, agencies, and agent users use this skill to inspect competitor Facebook and Instagram ad activity, compare creative patterns, and prepare structured ad intelligence reports. It can also guide optional Meta Graph API queries when spend, impression, or demographic fields are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags unsafe package installation guidance.

Mitigation: Install and run the skill only in a disposable or isolated environment, and avoid using --break-system-packages.

Risk: The release evidence flags browser scraping with weakened sandboxing.

Mitigation: Keep Chromium sandboxing enabled where possible and run scraping with least privilege in an isolated environment.

Risk: The skill can use Meta API access tokens.

Mitigation: Use least-privilege, short-lived Meta tokens and run the API phase only when the user explicitly needs fields that require it.

Risk: Third-party API alternatives can expose research targets and API keys outside the local environment.

Mitigation: Get user approval before sending queries or credentials to third-party providers.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/abhishekj9621/skills/meta-ad-spy)
- [Meta Ad Library](https://www.facebook.com/ads/library/)
- [Meta for Developers](https://developers.facebook.com/)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [Meta Ad Library API Field Reference](artifact/references/field_reference.md)
- [Facebook Page ID Lookup](artifact/references/page_id_lookup.md)
- [Third-Party Alternatives](artifact/references/alternatives.md)
- [SearchAPI Meta Ad Library API](https://www.searchapi.io/docs/meta-ad-library-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline code blocks and optional JSON data from scraper or API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes competitive intelligence summaries, extracted ad fields, setup commands, and optional raw JSON outputs.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
