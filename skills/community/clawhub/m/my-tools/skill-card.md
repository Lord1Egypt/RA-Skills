## Description: <br>
Provides current time and date lookup plus mathematical expression calculation by running bundled local Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjtfzh](https://clawhub.ai/user/mjtfzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users use this skill to answer time or date questions from the local runtime and to calculate user-provided mathematical expressions through a bundled calculator script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence marks the skill suspicious because the calculator can run arbitrary Python expressions instead of only doing math. <br>
Mitigation: Review carefully before installing and replace the calculator's eval-based execution with a strict arithmetic parser before relying on it in sensitive environments. <br>
Risk: The skill instructs the agent to execute local scripts for time lookup and calculation. <br>
Mitigation: Run the skill in a restricted workspace and review script behavior before allowing command execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mjtfzh/my-tools) <br>
- [Publisher profile](https://clawhub.ai/user/mjtfzh) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text results from local script execution, with shell command guidance in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Time output reflects the local runtime clock. Calculator output echoes the expression and computed result, or a failure message.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
