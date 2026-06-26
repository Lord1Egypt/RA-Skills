## Description: <br>
mailprocess opens the Mali low-code builder in Chrome, submits the user's app-building request, and starts the build workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenjada45-maker](https://clawhub.ai/user/chenjada45-maker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and internal developers use this skill to send application requirements to the Mali low-code platform for internal tools, dashboards, forms, and quick prototypes. <br>

### Deployment Geography for Use: <br>
Global, where users have access to the Mali platform and any required internal network or VPN. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control Chrome and submit user text through a logged-in session without a clear final confirmation step. <br>
Mitigation: Use explicit invocations, install only in trusted internal workflows, and add a manual confirmation or draft-only mode before sending requests. <br>
Risk: Submitted requirements may contain secrets or sensitive business data. <br>
Mitigation: Avoid including credentials, tokens, customer data, or confidential business details in prompts sent to the Mali platform. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenjada45-maker/mailprocess) <br>
- [Mali low-code platform](https://lowcode.baidu-int.com/ai-coding) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown status text with shell command invocations when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open Chrome, fill a browser input, and click send in a logged-in Mali session.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
