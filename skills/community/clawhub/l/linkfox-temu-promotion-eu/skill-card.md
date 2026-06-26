## Description: <br>
Helps agents use LinkFox scripts for Temu EU Partner Promotion APIs to query promotion activities, inspect candidate goods, enroll goods, check operation status, update promotion goods, and download signed files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, operators, and developers can use this skill to automate Temu EU promotion workflows through LinkFox, including activity discovery, product enrollment, activity product queries, and price or quantity updates. It is intended for accounts that already have valid LinkFox and Temu seller authorization. <br>

### Deployment Geography for Use: <br>
Europe <br>

## Known Risks and Mitigations: <br>
Risk: Broad Temu API access through the generic proxy can affect APIs outside the intended promotion workflow. <br>
Mitigation: Prefer the dedicated EU promotion scripts and review the requested type and params before execution. <br>
Risk: Sensitive LinkFox and Temu access tokens may be saved locally or exposed in terminal logs and agent traces. <br>
Mitigation: Use least-privileged, revocable tokens; avoid pasting raw tokens into shared logs; and avoid storing tokens unless local access is appropriately restricted. <br>
Risk: The skill depends on a third-party LinkFox gateway to forward seller-account requests. <br>
Mitigation: Install and run it only when the LinkFox gateway is trusted for the target Temu seller account. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-temu-promotion-eu) <br>
- [API Reference](artifact/references/api.md) <br>
- [Access Token Guide](artifact/references/access-token.md) <br>
- [Authorization Flow](artifact/references/authorization-flow.md) <br>
- [Partner EU Promotion Catalog](artifact/references/partner-eu-catalog.md) <br>
- [Per-API Documentation Index](artifact/references/apis/README.md) <br>
- [Temu Partner EU Documentation](https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON request and response payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and a Temu accessToken or storeKey; EU promotion scripts default to site=eu, managementType=semi-managed, and tokenPurpose=product-inventory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
