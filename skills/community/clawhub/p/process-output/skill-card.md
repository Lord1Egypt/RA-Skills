## Description: <br>
Process Output formats assistant replies as machine-parseable openclaw-process JSON progress blocks for clients that render live progress panels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2719040953](https://clawhub.ai/user/2719040953) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users of compatible ClawHub or OpenClaw clients use this skill to make an agent emit structured progress and final-result events that a UI can parse and display. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Structured process blocks can be incompatible with normal chat clients or users expecting plain answers. <br>
Mitigation: Enable the skill only in compatible clients and honor explicit final-answer-only opt-out requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2719040953/process-output) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown containing fenced openclaw-process JSON blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Simple interactions use start and final events; longer tasks may include step updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
