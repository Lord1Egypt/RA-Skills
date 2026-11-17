## Description:

Provides agent guidance and Python scripts for calling LinkFox-mediated Temu Global Ads APIs for ad creation, modification, reporting, logs, and ROAS prediction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and developers use this skill to operate Temu Global advertising through LinkFox, including campaign creation, budget or ROAS changes, ad detail checks, reports, logs, and token setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use LinkFox and Temu seller-token access that may exceed the narrow ads workflow.

Mitigation: Use least-privilege Temu tokens and install only when this account authority is acceptable.

Risk: Gateway or token configuration could point to an unexpected endpoint.

Mitigation: Check that LINKFOX_* gateway environment variables point to expected LinkFox domains before running scripts.

Risk: Tokens and full API responses may be stored locally or exposed through command history and output files.

Mitigation: Avoid putting tokens in shell history where possible, protect ~/.linkfox, and protect project linkfox output files.

Risk: Ad creation, deletion, budget, ROAS, or payment-order actions can affect live commerce operations.

Mitigation: Manually confirm any creation, deletion, budget or ROAS change, and payment order before executing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-ads-global)
- [API reference](artifact/references/api.md)
- [Temu accessToken authorization](artifact/references/access-token.md)
- [Authorization flow](artifact/references/authorization-flow.md)
- [Partner Global Ads interface catalog](artifact/references/partner-global-catalog.md)
- [Ads API documentation index](artifact/references/apis/README.md)
- [Temu Partner Global documentation](https://partner-global.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON files]

**Output Format:** [Markdown guidance with Python command examples and JSON request/response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts save full API responses under linkfox/<date>/<session>/data and summarize large responses unless --inline is used.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
