## Description: <br>
Track questions Hans failed to answer and flag missing knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atiati82](https://clawhub.ai/user/atiati82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent maintainers use this skill to capture questions Hans cannot answer, record the missing knowledge, and review recurring gaps for later improvement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs the agent to run a local Python logger script that is not included in the artifact. <br>
Mitigation: Package, review, and scope the referenced log-knowledge-gap.py script before enabling the skill. <br>
Risk: Unanswered user questions may be persisted in a knowledge-gaps.md log. <br>
Mitigation: Enable the skill only when persistent logging is intended, and apply appropriate access, retention, and review controls to the log. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/atiati82/knowledge-gaps) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Natural-language response text, Markdown summaries, and shell command instructions for logging gaps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or updates a knowledge-gaps.md log when the required logger script is available and successfully run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
