## Description: <br>
A friendly greeting skill that responds to hello/你好 in multiple languages, tells the current time, and introduces the OpenClaw assistant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ernest8976](https://clawhub.ai/user/ernest8976) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to provide short, language-matched greetings, self-introductions, and offers of help at the start of a conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on routine greetings or identity questions when the user expects the broader assistant to continue with another task. <br>
Mitigation: Use it only for greetings and self-introduction, then hand off non-greeting requests to the base assistant. <br>
Risk: Time-of-day wording can be inaccurate if the agent does not have a reliable current-time signal. <br>
Mitigation: Mention time of day only when the current context provides it; otherwise keep the greeting time-neutral. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ernest8976/hunter-helloworld) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Short natural-language greeting text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Language-matched 1-3 sentence responses; no commands, external tools, or persistent memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
