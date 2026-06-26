## Description: <br>
GPT Go puts the assistant into a persistent, execution-first mode that minimizes routine confirmations and pauses at explicit high-risk boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[C-Joey](https://clawhub.ai/user/C-Joey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users invoke this skill when they want a conversation to move into a faster execution posture with fewer routine confirmations. It is intended for clear tasks where the assistant can inspect the environment directly while still pausing for destructive, sensitive, externally visible, production, or otherwise high-risk actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables a faster, lower-confirmation assistant mode that can be overused on sensitive or ambiguous work. <br>
Mitigation: Invoke it only when this posture is desired; turn it off or ask for step-by-step collaboration before sensitive, ambiguous, production, privacy, credential, publishing, payment, or destructive work. <br>
Risk: Short follow-up directives are treated as continued authorization for the current task. <br>
Mitigation: Use explicit stop, pause, or clarification instructions when the task should not continue automatically, and rely on the documented pause boundaries for high-risk actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/C-Joey/gpt-go) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Markdown and plain text behavioral guidance for an agent conversation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persistent for the current conversation until the user turns it off, asks for a different style, or higher-priority rules override it.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
