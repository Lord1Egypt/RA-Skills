## Description:

聘才猫（Pincaimao）劳动合同卫士 calls the Pincaimao Labor Contract Guard API to analyze labor contract files or pasted contract text and generate an assessment report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pincaimao](https://clawhub.ai/user/pincaimao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to send labor contract documents or pasted contract text to Pincaimao for automated contract analysis and a readable assessment report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Labor contracts may include personal, compensation, and employment details that are transmitted to Pincaimao for remote analysis.

Mitigation: Install and invoke the skill only when this transfer is intended, and redact unnecessary sensitive details before upload or text submission.

Risk: An incorrect or untrusted API key or dependency source can cause authentication failures or route setup through an unexpected source.

Mitigation: Confirm PCM_LABOR_CONTRACT_KEY is obtained from Pincaimao and install any pincaimao-basic dependency only from a trusted listing.

Risk: Uploaded files return COS object keys that can refer to sensitive contract documents.

Mitigation: Treat cos_key values and uploaded document references as sensitive and avoid sharing them outside the authenticated workflow.

## Reference(s):

- [Pincaimao Homepage](https://www.pincaimao.com)
- [Pincaimao Labor Contracts Skill Listing](https://clawhub.ai/pincaimao/skills/pincaimao-labor-contracts)
- [Pincaimao Agent Registration and API Key](https://www.pincaimao.com/agents/login?invite_code=uwqc)
- [Pincaimao API Base Endpoint](https://api.pincaimao.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with shell and Python code blocks, plus readable text or raw API answer output on request]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PCM_LABOR_CONTRACT_KEY; accepts either a contract file cos_key or direct contract text; uses blocking API responses by default.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
