## Description:

Legal Consulting Bundle provides Chinese legal consultation workflows for contract review, legal Q&A, compliance checks, labor disputes, IP protection, and debt collection using a local China-law knowledge base with optional DeepSeek responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daimingvip-a11y](https://clawhub.ai/user/daimingvip-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as small business owners, founders, individuals, and legal assistants use this skill to generate preliminary Chinese legal analysis, contract risk checks, compliance checklists, labor-dispute guidance, IP-protection guidance, and debt-collection guidance. The outputs are informational and should be reviewed by qualified legal counsel before being relied on.

### Deployment Geography for Use:

Global; legal content is scoped to China-law use cases.

## Known Risks and Mitigations:

Risk: Sensitive legal questions, contracts, personal identifiers, trade secrets, or privileged material may be sent to external DeepSeek processing.

Mitigation: Add a visible privacy notice, require explicit opt-in for third-party LLM use, and minimize or redact sensitive inputs before submission.

Risk: The consultation endpoint is exposed without authentication or rate limiting.

Mitigation: Require authentication, add rate limits, and enforce request-size limits before deployment.

Risk: Generated legal analysis can be incomplete, outdated, or inappropriate for a specific matter.

Mitigation: Present outputs as preliminary information only and require qualified legal review before reliance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daimingvip-a11y/skills/legal-consulting-bundle)
- [DeepSeek chat completions endpoint](https://api.deepseek.com/v1/chat/completions)
- [Civil Code knowledge base excerpt](artifact/knowledge_base/civil_code.md)
- [Contract law knowledge base excerpt](artifact/knowledge_base/contract_law.md)
- [Labor law knowledge base excerpt](artifact/knowledge_base/labor_law.md)
- [Company law knowledge base excerpt](artifact/knowledge_base/company_law.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance, Configuration]

**Output Format:** [Markdown-style Chinese legal analysis returned as text or JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call DeepSeek when DEEPSEEK_API_KEY is configured; otherwise returns built-in template responses.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact SKILL.md frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
