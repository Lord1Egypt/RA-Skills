## Description: <br>
Temu Ads US helps agents work with Temu Partner US advertising APIs through LinkFox gateway scripts for ad creation, modification, details, logs, ROAS prediction, eligible goods lookup, and mall-level reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and commerce operators use this skill to guide and run Temu US advertising workflows, including campaign creation, budget and ROAS updates, ad status changes, reporting, and operational log review. It is intended for users who already have LinkFox gateway access and Temu seller advertising authorization. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger live Temu advertising spend actions, including ad creation, budget changes, ROAS changes, status updates, and deletion. <br>
Mitigation: Require manual review of store, goodsId, budget, ROAS, status, and action intent before running create or modify commands. <br>
Risk: The skill requires sensitive LinkFox and Temu seller advertising credentials. <br>
Mitigation: Treat access tokens like passwords, avoid exposing them in shared shells or logs, and prefer short-lived or scoped operational practices where available. <br>
Risk: The local token helper can store Temu access tokens in a plaintext file. <br>
Mitigation: Avoid plaintext local storage when possible; if storeKey usage is necessary, restrict filesystem permissions and avoid raw-token listing in shared or logged environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-temu-ads-us) <br>
- [API Reference](references/api.md) <br>
- [Access Token Guide](references/access-token.md) <br>
- [Partner US Ads Catalog](references/partner-us-catalog.md) <br>
- [Temu Partner US Ad Create Documentation](https://partner-us.temu.com/documentation?menu_code=1e72b5cceef545ec8f9652b9e56dd054&sub_menu_code=7bc9231776304158a895e41a816b7805) <br>
- [Temu Partner US Ad Modify Documentation](https://partner-us.temu.com/documentation?menu_code=1e72b5cceef545ec8f9652b9e56dd054&sub_menu_code=0b7140898262428eb8a4b28609112651) <br>
- [Temu Partner US Mall Reports Documentation](https://partner-us.temu.com/documentation?menu_code=1e72b5cceef545ec8f9652b9e56dd054&sub_menu_code=595f05856989480aa03abd58da203047) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads; helper scripts print JSON responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and a Temu accessToken or storeKey for live gateway calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
