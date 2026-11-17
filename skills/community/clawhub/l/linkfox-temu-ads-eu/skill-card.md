## Description:

Temu EU Ads helps agents operate Temu Europe advertising workflows through LinkFox-provided tooling, including ad creation, ad details, reports, logs, ROAS prediction, eligible goods checks, and ad modification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Temu sellers, advertising operators, and developers use this skill to query, create, modify, and report on Temu EU search recommendation ads. It is intended for agent-assisted ad operations that require LinkFox authentication and Temu seller authorization.

### Deployment Geography for Use:

Europe (Temu EU marketplace)

## Known Risks and Mitigations:

Risk: The skill handles LinkFox and Temu seller credentials and can persist Temu access tokens locally.

Mitigation: Use an isolated environment, avoid production credentials unless the publisher and runtime are trusted, and keep token storage paths out of shared workspaces.

Risk: Endpoint override environment variables can redirect gateway traffic.

Mitigation: Check that LINKFOX_TOOL_GATEWAY, TEMU_API_BASE_URL, and STORE_API_BASE_URL are unset or intentionally configured before running scripts.

Risk: Ad modification operations may pause ads, delete ads, or change budget and ROAS settings.

Mitigation: Require explicit human confirmation before mutation operations, especially delete, pause, budget, ROAS, or payment-related actions.

Risk: Token listing can expose full access tokens when mask=false is used.

Mitigation: Keep token listing masked in shared logs and avoid printing unmasked credentials in agent transcripts.

## Reference(s):

- [API Reference](references/api.md)
- [Temu accessToken Authorization](references/access-token.md)
- [Onboarding](references/onboarding.md)
- [Partner EU Ads Catalog](references/partner-eu-catalog.md)
- [Ads API Documentation Index](references/apis/README.md)
- [Temu Partner EU Documentation](https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON files, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses saved to local files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Large responses are summarized in stdout while full responses are written under a linkfox session data directory.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
