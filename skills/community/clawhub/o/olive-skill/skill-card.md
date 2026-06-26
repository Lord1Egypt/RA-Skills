## Description: <br>
Apply Oliver's stable persona, values, decision models, communication style, and evidence standards when an agent reasons about risk, responsibility, authority, open source, technology, learning, collaboration, or public communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamliuxiaozhen](https://clawhub.ai/user/iamliuxiaozhen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent toward Oliver's documented judgment patterns for technical decision-making, risk assessment, open-source collaboration, and evidence-based communication. It is intended for advisory reasoning, not for inventing unsupported persona positions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence reasoning across a wide range of tasks, which may be too broad for strict domain-specific policy handling. <br>
Mitigation: Use it alongside narrower specialist skills or policies, and keep task-specific requirements explicit. <br>
Risk: An agent may invent persona positions outside the documented evidence. <br>
Mitigation: Require outputs to distinguish confirmed information, strong inference, and unknowns, and keep conclusions grounded in the reference files. <br>
Risk: High-impact decisions may be over-reliant on advisory persona guidance. <br>
Mitigation: Verify consequential claims with independent evidence and human review before acting. <br>


## Reference(s): <br>
- [Identity](references/identity.md) <br>
- [Values](references/values.md) <br>
- [Decision Models](references/decision-models.md) <br>
- [Voice](references/voice.md) <br>
- [Knowledge Sources](references/knowledge-sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown prose with structured reasoning when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution or external tool output is expected; guidance should remain bounded by the persona references.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
