## Description: <br>
LLM as Judge guides agents to request cross-model review of complex plans, code, architecture, and high-risk decisions before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ngmeyer](https://clawhub.ai/user/ngmeyer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to decide when to ask a separate model to review complex plans, architecture, code, security-sensitive work, financial systems, or stalled tasks. The skill provides activation criteria, model-pairing guidance, and judge prompt templates for structured review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cross-model review can require sharing confidential code, security designs, trading systems, or internal planning context with another model provider. <br>
Mitigation: Use the skill only with providers approved for the data being reviewed, and avoid including secrets or unnecessary confidential details. <br>
Risk: Judge output can be incorrect, vague, or over-scoped, which may lead agents to accept misleading review guidance. <br>
Mitigation: Require structured verdicts, scores, and specific actionable issues, then have the executor verify findings before making changes. <br>


## Reference(s): <br>
- [Judge Prompt Templates](references/judge-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown guidance with prompt templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces review criteria, verdict formats, and model-pairing guidance; it does not execute code or access local systems.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
