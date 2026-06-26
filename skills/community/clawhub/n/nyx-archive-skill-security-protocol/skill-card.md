## Description: <br>
Teaches an agent a structured security-vetting protocol for reviewing ClawHub skills before and after installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nyxur42](https://clawhub.ai/user/nyxur42) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to have an agent perform structured security vetting of ClawHub skills before installation, explain audit decisions, and guide post-install checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to inspect local artifact files and basic system state during a security review. <br>
Mitigation: Limit reviews to the intended skill artifact or workspace, and avoid unrelated private directories unless the user explicitly requests that inspection. <br>
Risk: Security assessments can become overconfident if the agent treats heuristic checks as proof of safety. <br>
Mitigation: Have the agent show evidence, call out uncertainty, and ask the user before acting on unresolved yellow flags. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/nyxur42/nyx-archive-skill-security-protocol) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples and security assessment text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no scripts or dependencies are included in the artifact evidence.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
