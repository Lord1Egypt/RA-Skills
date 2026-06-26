## Description: <br>
Use this skill when installing, upgrading, verifying, or publishing the EverMemory OpenClaw plugin and its companion skill, including local path install, npm install, ClawHub publish, and release-gate verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao321](https://clawhub.ai/user/jiehao321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install, upgrade, verify, and publish the EverMemory plugin and companion skill while following release gates and account checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publish commands can change public ClawHub or npm releases when run with authenticated accounts. <br>
Mitigation: Confirm the logged-in ClawHub and npm accounts, review the scripts, run release gates, and use npm dry-run before any real publish. <br>
Risk: Binding the EverMemory memory slot or restarting the gateway changes the target OpenClaw runtime. <br>
Mitigation: Confirm the target OpenClaw instance before binding or restarting, then run the verification script and inspect command output. <br>


## Reference(s): <br>
- [EverMemory Install/Publish Playbook](references/publish-and-install-playbook.md) <br>
- [ClawHub skill page](https://clawhub.ai/jiehao321/openclaw-evermemory-installer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes release-gate, account-login, install, publish, and verification steps for OpenClaw and npm workflows.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
