## Description: <br>
Draws a four-card Tarot spread with cryptographic randomness to help agents choose a direction when a prompt is vague or multiple approaches are equally valid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kc0bfv](https://clawhub.ai/user/kc0bfv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill as a low-stakes tie-breaker when a user delegates the approach, asks to let fate decide, or gives an ambiguous prompt with several reasonable paths. It should guide framing and next steps, not override clear instructions, safety, or correctness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Tarot reading may be mistaken for authority in consequential decisions. <br>
Mitigation: Use it only for casual, low-stakes tie-breaking and do not rely on it for security, data integrity, production deployment, financial, legal, medical, or other consequential decisions. <br>
Risk: Broad activation language could influence an agent even when the user has provided clear instructions. <br>
Mitigation: Skip the skill when the task has a clear path or the user asks not to use Tarot, and keep user instructions, safety, and correctness ahead of the card interpretation. <br>
Risk: Repeated draws can be used to rationalize a preferred answer. <br>
Mitigation: Use one draw per decision point; if the drawing script fails, report the failure and do not invent cards. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with an optional shell command and JSON card-draw output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The draw produces four cards and relative card-file paths; the agent should not simulate a draw if the script fails.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
