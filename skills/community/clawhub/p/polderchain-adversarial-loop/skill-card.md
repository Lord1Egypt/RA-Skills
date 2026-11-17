## Description:

Use when a hard decision should be argued out between several models (one proposes, others attack it, the result is rebuilt and a human gates the risky cases), when comparing a neutral answer with a Polderchain-guided one, or when an answer needs a record of where each of its claims came from. Local orchestration; nothing is sent to the hub unless you ask.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minmaxnn](https://clawhub.ai/user/minmaxnn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to compare model answers on difficult decisions through proposal, critique, role reversal, provenance labeling, and synthesis. Its output is advisory; a human reviews sensitive or unresolved decisions before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model debate can produce incorrect or misleading guidance, and a critic's confidence is not proof.

Mitigation: Treat results as advisory and require human review for sensitive decisions, materially unresolved objections, or failed calls or parsing.

Risk: Local loop records retain complete prompts and outputs, which may contain sensitive information.

Mitigation: Exclude secrets and personal data from prompts, protect local logs, and redact records before sharing.

## Reference(s):

- [Polderchain Adversarial Loop skill page](https://clawhub.ai/minmaxnn/skills/polderchain-adversarial-loop)
- [Spelunking agents](https://spelunking.ai/agents/)
- [Covenant API](https://spelunking.ai/wp-json/spelunking/v1/covenant)
- [Spelunking MCP](https://spelunking.ai/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Text, JSON, Markdown]

**Output Format:** [Structured advisory response with numbered claims, objections, provenance labels and a recommendation; JSON/JSONL and Markdown record formats are described.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory only. Human review is required for sensitive or unresolved cases. The package provides instructions and record formats, not a runner.]

## Skill Version(s):

0.9.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
