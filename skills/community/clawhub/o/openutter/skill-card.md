## Description: <br>
Headless Google Meet bot that joins meetings and captures live captions as transcripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sumansid](https://clawhub.ai/user/sumansid) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to join Google Meet calls with a meeting bot, capture live captions as transcripts, and request meeting screenshots for visual context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bot can capture and share sensitive meeting visuals and transcripts. <br>
Mitigation: Use only with appropriate participant consent, set a duration or stop the bot when done, and protect or delete saved transcripts and screenshots after use. <br>
Risk: A saved Google session can be reused by the bot. <br>
Mitigation: Prefer guest mode or a dedicated low-privilege Google account, and protect or delete ~/.openutter/auth.json after use. <br>
Risk: The release evidence reports an unsafe shell command path and browser automation that may disguise automation. <br>
Mitigation: Review commands before execution, run in a constrained environment, and install only after accepting the security guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sumansid/openutter) <br>
- [OpenUtter homepage](https://github.com/sumansid/openutter) <br>
- [Recall.ai Google Meet bot reference](https://www.recall.ai/blog/how-i-built-an-in-house-google-meet-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and transcript or screenshot file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local transcript text files and meeting screenshot image files during bot operation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
