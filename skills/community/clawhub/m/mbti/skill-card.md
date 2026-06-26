## Description: <br>
MBTI diagnoses an agent personality type, compares it with user expectations, and generates configuration change suggestions for agent behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[torchesfrms](https://clawhub.ai/user/torchesfrms) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use MBTI to assess an agent's self-reported and measured behavior, compare it with a desired personality profile, and prepare configuration suggestions for SOUL.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose persistent SOUL.md configuration changes without sufficient user control or rollback guidance. <br>
Mitigation: Treat outputs as proposals; require the agent to show the exact SOUL.md diff, explain scope, create a backup, and receive explicit approval before writing changes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command output and proposed configuration patches] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent SOUL.md changes that require explicit review before writing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
