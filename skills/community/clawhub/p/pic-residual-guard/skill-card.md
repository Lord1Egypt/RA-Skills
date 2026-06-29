## Description: <br>
OpenClaw agent safety checklist for action review, risk assessment, rollback planning, and LLM output validation before external effects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kadubon](https://clawhub.ai/user/kadubon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to make agents pause before external-effect actions, create an action proposal, identify evidence gaps and rollback paths, classify risk, and require confirmation for high-risk or sensitive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may treat advisory review notes, proposed commands, or PIC report fields as permission to act. <br>
Mitigation: Treat proposals and PIC reports as review data only; require evidence, scope, approval, and rollback checks before any external-effect action. <br>
Risk: Sensitive external-effect actions can involve credentials, installs, file deletion, network requests, payments, or irreversible transactions. <br>
Mitigation: Block or require explicit human confirmation for high-risk, critical, credential-related, install-related, payment-related, or irreversible actions. <br>


## Reference(s): <br>
- [Project repository](https://github.com/kadubon/pic-openclaw-skill) <br>
- [ClawHub skill page](https://clawhub.ai/kadubon/pic-residual-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown] <br>
**Output Format:** [Markdown guidance with structured action-review checklist text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory review output only; the skill does not execute proposed actions.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
