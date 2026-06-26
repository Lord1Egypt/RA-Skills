## Description: <br>
Helps agents use LinkFox-forwarded Temu Global cancel-order APIs for buyer after-sales cancellation and seller appeal or out-of-stock cancellation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Temu sellers and operators use this skill to list pending buyer cancellation requests, agree to buyer cancellations, submit seller cancellation appeals, submit out-of-stock cancellations, and check cancellation results for Temu Global orders. <br>

### Deployment Geography for Use: <br>
Global, for Temu Global and Partner-region cancellation workflows outside the separate US and EU variants. <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles LinkFox credentials and Temu seller access tokens that can authorize sensitive seller operations. <br>
Mitigation: Use least-privilege, short-lived tokens; avoid local token storage where possible; and protect or delete ~/.linkfox/temu-access-tokens.json after use. <br>
Risk: Cancellation calls can change order or after-sales state. <br>
Mitigation: Require explicit human confirmation and verify order identifiers, store context, site, and token purpose before executing any state-changing call. <br>
Risk: The artifact includes broader Temu gateway and file-download helpers beyond the named cancel-order workflow. <br>
Mitigation: Restrict use to documented cancel-order API types unless the operator has reviewed and approved the broader gateway or file-download action. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [Temu Access Token Authorization](references/access-token.md) <br>
- [Authorization Flow](references/authorization-flow.md) <br>
- [Partner Global Cancel Order Catalog](references/partner-global-catalog.md) <br>
- [Cancel Order API Index](references/apis/README.md) <br>
- [Temu Partner Global Documentation](https://partner-global.temu.com/documentation) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with bash examples and JSON request or response payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY plus a Temu accessToken or storeKey; some scripts can change order state.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
