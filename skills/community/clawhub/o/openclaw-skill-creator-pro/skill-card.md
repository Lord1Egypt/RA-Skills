## Description: <br>
Teach your OpenClaw agent new abilities by creating custom skills from plain-English requests, including setup and testing guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kennyzir](https://clawhub.ai/user/kennyzir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to generate new OpenClaw skill files, installation steps, testing prompts, and troubleshooting guidance for workflow-specific agent capabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated skills may require API credentials for services such as Slack or Google Calendar. <br>
Mitigation: Use least-privilege credentials, store secrets outside skill files, and review generated configuration before enabling the skill. <br>
Risk: Generated skills may send messages, read local files, or handle sensitive workflow data. <br>
Mitigation: Review generated code and add confirmation steps before actions that send messages or process sensitive data. <br>
Risk: Generated skill code or setup guidance may be incomplete or unsuitable for a specific environment. <br>
Mitigation: Test each generated skill in a controlled environment and scan it before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kennyzir/openclaw-skill-creator-pro) <br>
- [OpenClaw Skill Creator documentation](https://claw0x.com/docs/openclaw-skill-creator) <br>
- [Google Calendar API quickstart](https://developers.google.com/calendar/api/quickstart/nodejs) <br>
- [Slack API quickstart](https://api.slack.com/start/quickstart) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with TypeScript code blocks, installation steps, testing prompts, and troubleshooting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated examples may reference local files, Slack, Google Calendar, or other services depending on the requested skill.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
