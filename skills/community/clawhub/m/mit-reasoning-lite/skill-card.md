## Description: <br>
Provides a 3-step reasoning scaffold that prompts agents to clarify objectives, check constraints, and state reasoning before significant actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kgapol](https://clawhub.ai/user/kgapol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to add a lightweight decision checkpoint before high-impact, ambiguous, or hard-to-reverse actions. It is intended to improve reasoning discipline by asking the agent to clarify the objective, check constraints, and explain its rationale before acting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled install.sh references README.md and USAGE.md files that are not present in the release artifact. <br>
Mitigation: Install through ClawHub or manually copy SKILL.md; review shell output before relying on installer completion. <br>
Risk: As a prompt-only reasoning scaffold, it can structure explanations but does not independently verify that a decision is correct or policy-compliant. <br>
Mitigation: Keep human review and existing policy checks for high-impact actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kgapol/mit-reasoning-lite) <br>
- [Trust AI Stack on ClawMart](https://www.shopclawmart.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only reasoning scaffold; no runtime service or API output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
