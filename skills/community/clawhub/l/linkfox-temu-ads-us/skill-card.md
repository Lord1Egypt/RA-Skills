## Description:

Temu美国站-广告 helps agents use LinkFox gateway scripts and references for Temu US Partner Ads APIs, including ad creation, modification, detail queries, reporting, logs, ROAS prediction, and eligible-goods checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and marketplace operators use this skill to inspect and run Temu US advertising API calls through LinkFox for campaign creation, budget and ROAS changes, reporting, logs, file download, and credential onboarding.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill handles LinkFox and Temu credentials that can read or change ad settings.

Mitigation: Install only if LinkFox is trusted; prefer per-session credentials or a secure credential manager and rotate any exposed keys.

Risk: The arbitrary proxy can perform broader Temu gateway calls than the named Ads scripts.

Mitigation: Use named ads scripts for routine tasks and reserve the arbitrary proxy for intentional broader access.

Risk: Saved linkfox/ outputs and shell profiles can expose operational or credential-adjacent data.

Mitigation: Avoid committing linkfox/ outputs or shell profiles, and review saved response files before sharing a workspace.

Risk: Onboarding support includes payment-order creation flows.

Mitigation: Run billing order commands only when intentionally resolving a billing issue and after confirming the plan and payment method.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-ads-us)
- [API reference](artifact/references/api.md)
- [Partner US Ads catalog](artifact/references/partner-us-catalog.md)
- [Ads API document index](artifact/references/apis/README.md)
- [Temu accessToken authorization](artifact/references/access-token.md)
- [Authentication and billing onboarding](artifact/references/onboarding.md)
- [Temu Partner documentation: temu.searchrec.ad.roas.pred](https://partner-us.temu.com/documentation?menu_code=1e72b5cceef545ec8f9652b9e56dd054&sub_menu_code=dfff26bad8e94ed5abaaf5cdade50c26)
- [Temu Partner documentation: temu.searchrec.ad.reports.mall.query](https://partner-us.temu.com/documentation?menu_code=1e72b5cceef545ec8f9652b9e56dd054&sub_menu_code=595f05856989480aa03abd58da203047)
- [Temu Partner documentation: temu.searchrec.ad.create](https://partner-us.temu.com/documentation?menu_code=1e72b5cceef545ec8f9652b9e56dd054&sub_menu_code=7bc9231776304158a895e41a816b7805)
- [Temu Partner documentation: temu.searchrec.ad.detail.query](https://partner-us.temu.com/documentation?menu_code=1e72b5cceef545ec8f9652b9e56dd054&sub_menu_code=66db5438c37446f49c122829489ac6d4)
- [Temu Partner documentation: temu.searchrec.ad.log.query](https://partner-us.temu.com/documentation?menu_code=1e72b5cceef545ec8f9652b9e56dd054&sub_menu_code=c2c5eda51c414e788bab914a297d1881)
- [Temu Partner documentation: temu.searchrec.ad.goods.create.query](https://partner-us.temu.com/documentation?menu_code=1e72b5cceef545ec8f9652b9e56dd054&sub_menu_code=374d1f7fefdb4232b7b7a0239cb4465d)
- [Temu Partner documentation: temu.searchrec.ad.modify](https://partner-us.temu.com/documentation?menu_code=1e72b5cceef545ec8f9652b9e56dd054&sub_menu_code=0b7140898262428eb8a4b28609112651)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands; scripts emit JSON to stdout and save response JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are saved under linkfox/<date>/<session>/data; large responses print summaries unless --inline is used.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
