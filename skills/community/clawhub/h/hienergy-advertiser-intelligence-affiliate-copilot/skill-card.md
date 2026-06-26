## Description: <br>
HiEnergy Advertiser Intelligence Affiliate Copilot helps agents query HiEnergy API v1 for affiliate advertiser discovery, deal and program research, transaction and commission analysis, status changes, publisher details, and partner contacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyptkarsh](https://clawhub.ai/user/flyptkarsh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Affiliate marketing operators, partner marketing teams, and agent developers use this skill to search HiEnergy advertiser, program, deal, transaction, commission, publisher, and contact data. It is intended for workflows where an authenticated HiEnergy API key grants access to the same business data the user can see in the HiEnergy web app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive HiEnergy affiliate business data, including contacts and transaction or commission information. <br>
Mitigation: Install only for agents that need this data, use a least-privilege HiEnergy API key, and avoid running debug scripts in shared logs or CI. <br>
Risk: The skill includes remote write actions such as contact creation, contact reassignment, or publisher updates. <br>
Mitigation: Require explicit human approval before any contact creation, contact reassignment, or publisher update. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/flyptkarsh/hienergy-advertiser-intelligence-affiliate-copilot) <br>
- [HiEnergy homepage](https://www.hienergy.ai) <br>
- [HiEnergy API documentation](https://app.hienergy.ai/api_documentation) <br>
- [Endpoint reference](references/endpoints.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown summaries with optional Python or shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HIENERGY_API_KEY or HI_ENERGY_API_KEY and accesses https://app.hienergy.ai API data visible to that user.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
