## Description: <br>
嘴替 Skill acts as a universal query preprocessor that restates user intent, identifies domain and task context, asks limited clarifying questions, and produces a structured Query Plan plus rewritten professional prompt for downstream agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longsasasasasa](https://clawhub.ai/user/longsasasasasa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to turn informal or incomplete requests into clarified, structured prompts before handing work to a downstream agent or model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill attempts to act as a persistent front door for nearly all user requests. <br>
Mitigation: Install only when that behavior is intended, manually review any AGENTS.md or SOUL.md changes, and keep a rollback path. <br>
Risk: The learning-profile behavior may store user query-pattern preferences without enough control or privacy detail. <br>
Mitigation: Leave the learning profile disabled unless users explicitly consent to storing their query-pattern preferences. <br>
Risk: High-risk legal, medical, financial, tax, or psychological prompts could be over-clarified into advice-like outputs. <br>
Mitigation: Restrict outputs in those domains to information organization, clarification, and risk identification, and direct users to qualified professionals for formal advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/longsasasasasa/prompt-boost-skill) <br>
- [Activation Guide](artifact/references/activation-guide.md) <br>
- [Output Contract](artifact/references/output-contract.md) <br>
- [Risk Guardrails](artifact/references/risk-guardrails.md) <br>
- [Learning Profile](artifact/references/learning-profile.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance, Configuration] <br>
**Output Format:** [Markdown sections with a structured Query Plan and JSON handoff payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Clarification responses are capped at three questions per turn and the workflow forces convergence after three clarification rounds.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
