## Description: <br>
HS Code Lookup for Chinese Products. Query customs codes, tariff rates, declaration elements, and regulatory requirements via HSCIQ MCP API. Create classification consultation requests with image upload for expert review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toucao](https://clawhub.ai/user/toucao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, trade operators, and agents use this skill to query Chinese product HS codes, tariff details, declaration elements, regulatory requirements, CIQ data, hazardous-goods data, port information, and classification examples. It can also create and manage HSCIQ classification consultation records for expert review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an HSCIQ API key and sends selected product information to the HSCIQ service. <br>
Mitigation: Install only when the operator is comfortable granting the skill that credential, and scope or rotate the API key according to the HSCIQ account policy. <br>
Risk: The skill can create external consultation records, upload product images, and post discussion replies. <br>
Mitigation: Require the agent to show the exact fields, files, and action before creating consultations, uploading images, or posting replies, then proceed only after explicit user approval. <br>
Risk: Uploaded product images or consultation text may contain sensitive commercial information. <br>
Mitigation: Review files and product details before submission and avoid sending confidential or regulated data unless the user has approved that disclosure. <br>


## Reference(s): <br>
- [HSCIQ MCP API Documentation](https://www.hsciq.com/MCP/Docs) <br>
- [HSCIQ Service](https://www.hsciq.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/toucao/hsciq-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an HSCIQ API key; API calls can return customs-code data, consultation records, and discussion responses.] <br>

## Skill Version(s): <br>
2.0.7 (source: server release metadata, created 2026-05-12T15:38:51.532Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
