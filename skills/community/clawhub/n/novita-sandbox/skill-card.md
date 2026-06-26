## Description: <br>
Run browser operations and untrusted code in an isolated Novita cloud sandbox using Firecracker microVMs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[piston4711](https://clawhub.ai/user/piston4711) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run external browsing tasks, downloaded code, build commands, and unfamiliar project workflows in a Novita cloud sandbox instead of the local workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can upload selected local files to a cloud sandbox. <br>
Mitigation: Do not upload secrets, credentials, API keys, personal configuration, or other sensitive local files. <br>
Risk: The helper can write downloaded sandbox files back to local paths. <br>
Mitigation: Download only to explicit safe destinations and inspect expected outputs before relying on them. <br>
Risk: Sandbox use requires a Novita API key and may run remote commands with internet access. <br>
Mitigation: Use the skill only when comfortable with remote sandbox execution, protect the API key, and kill sandboxes after sensitive work. <br>


## Reference(s): <br>
- [Novita Sandbox: Browser Use Integration](references/browser-use.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/piston4711/novita-sandbox) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash, Python, and JavaScript command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sandbox command output is JSON and may be truncated by the helper script.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
