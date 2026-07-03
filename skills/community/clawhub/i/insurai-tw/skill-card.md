## Description: <br>
Supports Republic of China (Taiwan) personal insurance workflows through the InsurAI Agent API, including planning interpretation, occupation lookup, product recommendation and search, metadata lookup, document retrieval, and PDF link lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[riseliu](https://clawhub.ai/user/riseliu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to answer supported Taiwan personal insurance questions by applying scope rules, normalizing inputs, calling InsurAI Agent API actions, and summarizing returned planning, product, occupation, document, or PDF-link data. <br>

### Deployment Geography for Use: <br>
Republic of China (Taiwan) <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles API keys and sensitive Taiwan insurance planning details with weak safety boundaries. <br>
Mitigation: Review before installing, provide the API key through a secret mechanism, do not echo or paste keys into chats or logs, and avoid sending unnecessary personal, health-adjacent, or financial details. <br>
Risk: Requests are sent to the InsurAI endpoint and may include user insurance planning details. <br>
Mitigation: Use this skill only when the InsurAI endpoint is trusted and keep TLS verification enabled unless an approved CA bundle or environment requires another explicit setting. <br>
Risk: Unsupported or out-of-scope insurance questions could lead to misleading guidance if the skill continues after a rejection condition or API error. <br>
Mitigation: Apply the documented Taiwan personal insurance scope, mandatory rejection rules, supported insurer list, and endpoint-specific stop conditions before relying on API results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/riseliu/skills/insurai-tw) <br>
- [InsurAI Agent API endpoint](https://insurai.com.tw/insurai/agent) <br>
- [InsurAI Taiwan business rules](references/insurai-rules.md) <br>
- [InsurAI REST API contract](references/insurai-api-spec.md) <br>
- [InsurAI API script reference](references/insurai-api-script.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and summarized JSON/API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires INSURAI_AGENT_URL, INSURAI_API_KEY, and TLS settings; outputs should summarize relevant API fields instead of dumping raw JSON.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter, VERSION, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
