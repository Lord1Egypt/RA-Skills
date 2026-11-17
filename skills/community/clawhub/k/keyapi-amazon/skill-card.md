## Description:

Explore and analyze Amazon marketplace data through the KeyAPI REST API using live official docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyzzero](https://clawhub.ai/user/xyzzero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and marketplace operators use this skill to turn Amazon marketplace research requests into documentation-guided KeyAPI workflows for product discovery, category research, ranking checks, seller intelligence, influencer storefront research, reviews, offers, and ASIN/GTIN conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup helper can persist a KeyAPI token into shell startup profile files in plaintext.

Mitigation: Prefer setting KEYAPI_TOKEN only for the current shell session or using a dedicated credential store, avoid passing tokens on the command line, and install only when plaintext shell-profile storage is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xyzzero/skills/keyapi-amazon)
- [KeyAPI documentation index](https://docs.keyapi.ai/llms.txt)
- [KeyAPI authentication](https://docs.keyapi.ai/overview/authentication#bearer-authentication)
- [KeyAPI dashboard](https://keyapi.ai/app/dashboard)
- [Amazon rules](references/amazon-rules.md)
- [Scenario cards](references/scenarios.md)
- [Routing policy](references/routing-policy.md)
- [Setup and auth](references/setup-and-auth.md)
- [Amazon product module rules](references/amazon-product-rules.md)
- [Amazon seller module rules](references/amazon-seller-rules.md)
- [Amazon influencer module rules](references/amazon-influencer-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute live KeyAPI REST calls when credentials are available; large API responses can be saved to JSON files when requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
