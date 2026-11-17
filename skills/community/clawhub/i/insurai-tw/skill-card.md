## Description:

InsurAI Taiwan Personal Insurance helps agents handle Republic of China (Taiwan) personal insurance planning, product lookup, recommendations, policy review, coverage-gap analysis, and document retrieval through the InsurAI Agent API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jrsoft-insurai](https://clawhub.ai/user/jrsoft-insurai)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to support Taiwan personal insurance workflows, including planning interpretation, occupation classification, product search and recommendation, policy review, coverage-gap analysis, and insurance document retrieval. It requires user consent before sending necessary insurance or planning inputs to the configured InsurAI Agent API endpoint.

### Deployment Geography for Use:

Republic of China (Taiwan)

## Known Risks and Mitigations:

Risk: Sensitive insurance, personal, or financial details may be transmitted to the configured InsurAI Agent API endpoint.

Mitigation: Require explicit consent before the first API call, submit only minimum necessary fields, and avoid unnecessary identifiers such as national ID numbers, contact details, full policy documents, payment data, or medical records.

Risk: A configurable INSURAI_AGENT_URL could send API traffic and API-key-authenticated requests to an untrusted endpoint.

Mitigation: Keep INSURAI_AGENT_URL pinned to a trusted HTTPS InsurAI endpoint and review the endpoint before execution.

Risk: Policy images or PDFs may require external OCR or document processing before this skill can analyze the extracted text.

Mitigation: Obtain consent before using any OCR or document-processing service and send only extracted text and follow-up inputs needed for the analysis.

## Reference(s):

- [InsurAI Taiwan Dev Business Rules](references/insurai-rules.md)
- [InsurAI REST API Endpoint Contract](references/insurai-api-spec.md)
- [insurai_api.py Script Reference](references/insurai-api-script.md)
- [Policy Review and Coverage-Gap Workflow](references/policy-review-workflow.md)
- [InsurAI Website](https://insurai.com.tw)
- [Default InsurAI Agent API Endpoint](https://insurai.com.tw/insurai/agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summaries with optional JSON API results and shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires INSURAI_API_KEY; API calls use the configured HTTPS INSURAI_AGENT_URL and should minimize personal insurance data.]

## Skill Version(s):

1.0.6 (source: SKILL.md frontmatter, VERSION, README.md, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
