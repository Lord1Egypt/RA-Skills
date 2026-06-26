## Description: <br>
聘才猫（Pincaimao）劳动合同卫士 helps an agent call the Pincaimao Labor Contract Guard API to analyze a labor contract from an uploaded file key or pasted text and generate an assessment report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pincaimao](https://clawhub.ai/user/pincaimao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route labor contract files or pasted contract text to Pincaimao for contract analysis and a readable assessment report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Labor contracts or pasted contract text are sent to api.pincaimao.com for AI processing. <br>
Mitigation: Use this skill only for contracts that may be shared with Pincaimao; redact personal, salary, address, and confidential business terms where possible. <br>
Risk: Uploaded files are stored on Pincaimao's Cloud Object Storage and returned cos_key paths are sensitive. <br>
Mitigation: Treat cos_key values as sensitive and verify the provider's retention and deletion policies before using the skill with confidential contracts. <br>
Risk: The security verdict is suspicious because the skill handles sensitive contract data through a third-party API. <br>
Mitigation: Review organizational sharing rules and provider terms before deployment, and avoid using the skill for contracts that cannot be sent to external services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pincaimao/pincaimao-labor-contracts) <br>
- [Pincaimao homepage](https://www.pincaimao.com) <br>
- [Pincaimao API endpoint](https://api.pincaimao.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and Python examples; API responses may be summarized as readable text or shown as raw output on request.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PCM_LABOR_CONTRACT_KEY, curl, and python3; accepts either a file cos_key or direct contract text.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
