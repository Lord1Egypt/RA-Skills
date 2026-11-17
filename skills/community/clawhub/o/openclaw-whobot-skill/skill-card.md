## Description:

Provides a WhoBot (呼波特) AI phone digital employee knowledge base for answering questions about company information, product capabilities, core technologies, business scenarios, industry cases, team, compliance, and related WhoBot topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whobot-ai](https://clawhub.ai/user/whobot-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer WhoBot-related questions and expose a local knowledge service with FAQ, overview, and keyword search over the bundled knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Human-like AI calling and customer-data workflows can require disclosure, consent, retention, and access-control review.

Mitigation: Before customer-facing use, require clear AI disclosure, lawful recording consent, retention limits, access controls, and workflow-specific review for healthcare, telecom, sales, or support deployments.

Risk: HTTP mode can expose the knowledge service on a reachable interface if enabled without network controls.

Mitigation: Prefer local stdio use; enable HTTP only behind authenticated access, network restrictions, and request limits.

## Reference(s):

- [WhoBot Knowledge Base](references/knowledge.md)
- [WhoBot Homepage](https://www.whobot.com)
- [ClawHub Skill Page](https://clawhub.ai/whobot-ai/skills/openclaw-whobot-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Plain text and Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the bundled WhoBot knowledge base; release metadata lists gh as a required binary.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
