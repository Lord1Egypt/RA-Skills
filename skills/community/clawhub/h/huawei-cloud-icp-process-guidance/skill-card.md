## Description:

Provides Chinese-language question answering and process guidance for Huawei Cloud ICP filing using a bundled knowledge base, with optional web-search fallback for uncovered or time-sensitive questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support agents use this skill to answer Huawei Cloud ICP filing questions about prerequisites, materials, workflow steps, review status, rejection handling, authorization codes, changes, cancellation, migration, and App filing. The skill is scoped to Huawei Cloud ICP filing and should decline unrelated cloud, pricing, purchasing, or non-filing questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional web-search fallback can send user queries to agent-reach and Exa as an external data flow.

Mitigation: Avoid putting identity numbers, account details, or other sensitive filing data in prompts that may trigger search, and review the agent-reach dependency before enabling fallback search.

Risk: ICP filing rules and regional regulator requirements can change, so bundled knowledge-base answers may become outdated.

Mitigation: Use the documented search fallback for latest-policy questions, preserve official-source disclaimers, and review the answer against Huawei Cloud or regulator guidance before relying on it.

Risk: The skill is intentionally scoped and may give misleading help if used for other cloud providers, pricing, purchasing, or unrelated technical issues.

Mitigation: Keep the Huawei Cloud ICP filing boundary checks and refusal behavior enabled for out-of-scope requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-icp-process-guidance)
- [Knowledge base overview](kb/overview.md)
- [Knowledge base index](kb/index.md)
- [Search fallback strategy](references/search-fallback.md)
- [Verification method](references/verification-method.md)
- [Acceptance criteria](references/acceptance-criteria.md)
- [IAM policies](references/iam-policies.md)
- [Agent Reach installation guide](https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md)
- [Agent Reach troubleshooting](https://github.com/Panniantong/agent-reach/blob/main/docs/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown briefing answer with source notes and optional shell commands for setup or search fallback.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should be concise, source-attributed, limited to Huawei Cloud ICP filing, and include a search-result disclaimer when web search is used.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
