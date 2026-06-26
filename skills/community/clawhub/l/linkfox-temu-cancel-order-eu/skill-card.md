## Description: <br>
Temu Cancel Order EU helps agents guide and run LinkFox gateway scripts for Temu Partner EU buyer and seller order-cancellation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, operators, and developers use this skill to list and agree buyer cancellation requests, submit seller cancellation appeals or out-of-stock cancellations, and check cancellation results for Temu Partner EU orders through LinkFox. <br>

### Deployment Geography for Use: <br>
Europe (Temu Partner EU workflows) <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes broad authenticated Temu gateway, proxy, and file-download capabilities beyond the narrow EU cancel-order workflow. <br>
Mitigation: Install only when that authority is intended, prefer the six dedicated cancellation scripts, and avoid generic proxy or file-download helpers unless the Temu API call is understood. <br>
Risk: The workflow handles sensitive LinkFox and Temu tokens, and the artifact supports saving Temu access tokens in a local plaintext store. <br>
Mitigation: Avoid plaintext token storage on shared, backed-up, or synced machines, keep credentials out of logs, prompts, shell history, and shared files, and rotate any token that may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-temu-cancel-order-eu) <br>
- [API reference](references/api.md) <br>
- [Partner EU cancel order catalog](references/partner-eu-catalog.md) <br>
- [Access token guide](references/access-token.md) <br>
- [Authorization flow](references/authorization-flow.md) <br>
- [Per-interface API documents](references/apis/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct users to provide LinkFox and Temu credentials before running API helper scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
