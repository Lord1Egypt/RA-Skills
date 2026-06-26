## Description: <br>
Temu Ads EU helps agents work with LinkFox-gatewayed Temu Partner EU advertising APIs for ad creation, modification, reporting, ROAS prediction, operation logs, and signed file downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators managing Temu EU storefront advertising can use this skill to prepare and run LinkFox-mediated API calls for campaign creation, budget or ROAS changes, ad status updates, reporting, and log queries. The skill is most relevant when the agent has an approved LinkFox API key and a Temu accessToken or storeKey for the target shop. <br>

### Deployment Geography for Use: <br>
Europe (Temu EU and Partner EU workflows) <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live ad-spend or campaign-state changes through create and modify endpoints. <br>
Mitigation: Confirm every create, delete, pause, budget, and ROAS change before execution, and prefer the narrower eu_ads_* scripts over the generic proxy when possible. <br>
Risk: The skill requires sensitive LinkFox and Temu credentials and can optionally save Temu tokens locally. <br>
Mitigation: Use environment variables or a protected token store, avoid saving tokens unless needed, and do not print raw tokens in shared terminals, logs, or agent transcripts. <br>
Risk: The generic proxy can forward broader Temu requests than the named Ads helper scripts. <br>
Mitigation: Restrict proxy use to the documented Temu EU Ads types and review the request payload against the Partner EU API reference before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-temu-ads-eu) <br>
- [API reference](references/api.md) <br>
- [Temu accessToken authorization](references/access-token.md) <br>
- [Partner EU API catalog](references/partner-eu-catalog.md) <br>
- [Ads endpoint index](references/apis/README.md) <br>
- [Temu Partner EU documentation](https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with JSON payload examples and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LinkFox API credentials plus a Temu accessToken or storeKey; some scripts can call live advertising APIs or read/write a local token store.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
