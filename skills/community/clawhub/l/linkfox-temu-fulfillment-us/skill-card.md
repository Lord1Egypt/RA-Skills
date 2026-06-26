## Description: <br>
Temu Fulfillment US helps agents work with Temu US fulfillment APIs for buy-shipping labels, co-warehouse fulfillment, self-fulfilled shipments, tracking, scan forms, and related shipment operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and marketplace operators use this skill to guide Temu US fulfillment workflows, including creating and updating shipments, retrieving labels and documents, scheduling pickup reservations, and checking tracking information. It is intended for agents assisting with LinkFox-mediated Temu shipping operations that require valid LinkFox and Temu credentials. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to create, update, confirm, or cancel real Temu shipments. <br>
Mitigation: Review shipment identifiers, package details, and cancellation or confirmation intent before running generated commands. <br>
Risk: The workflow uses Temu accessToken values and LINKFOXAGENT_API_KEY credentials. <br>
Mitigation: Use secure secret storage, avoid pasting live credentials into chat or shell history, and restrict local token-store file permissions. <br>
Risk: Local token storage may persist sensitive Temu access tokens under the user's home directory or a configured token-store path. <br>
Mitigation: Use the token store only on trusted machines, set a protected TEMU_TOKEN_STORE_PATH when needed, and rotate exposed tokens promptly. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/linkfox-ai/linkfox-temu-fulfillment-us) <br>
- [Temu accessToken authorization and retrieval](references/access-token.md) <br>
- [Temu authorization flow](references/authorization-flow.md) <br>
- [LinkFox Temu gateway API](references/api.md) <br>
- [Partner US fulfillment catalog](references/partner-us-catalog.md) <br>
- [Fulfillment API documentation index](references/apis/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include executable Python script invocations and Temu or LinkFox API request bodies.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
