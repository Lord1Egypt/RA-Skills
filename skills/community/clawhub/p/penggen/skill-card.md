## Description: <br>
Applies a Chinese crosstalk-style supportive persona to agent responses, adding short setup lines and optional closing remarks while preserving the user's requested answer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataelf](https://clawhub.ai/user/dataelf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an assistant to answer with brief Chinese crosstalk-style encouragement while still completing ordinary work such as coding, research, planning, or conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The crosstalk-style tone can be inappropriate for formal writing, non-Chinese conversations, serious incidents, or situations where exact tone and brevity matter. <br>
Mitigation: Enable the skill only where this tone is desired, and disable or bypass it for formal, non-Chinese, serious, or highly concise workflows. <br>
Risk: Persona text can add prefaces or closing remarks that distract from technical answers or reduce brevity. <br>
Mitigation: Review outputs for task fit and keep persona text short; the artifact directs the agent not to insert persona content inside code or technical answers and to answer directly in urgent cases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataelf/penggen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with task-specific code blocks when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tone-shaping persona; the skill directs the agent to answer directly for serious or urgent situations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
