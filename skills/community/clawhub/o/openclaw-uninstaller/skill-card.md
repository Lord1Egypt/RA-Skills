## Description: <br>
OpenClaw 卸载指南，帮你体面告别这只昂贵的龙虾 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dox012](https://clawhub.ai/user/dox012) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to get concise OpenClaw removal guidance across macOS, Linux, and Windows. It provides one-click uninstall commands, manual cleanup steps, service removal commands, and follow-up troubleshooting references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The uninstall guidance includes destructive deletion commands such as non-interactive uninstall and recursive removal of OpenClaw state directories. <br>
Mitigation: Confirm resolved target paths and back up OpenClaw configuration or workspace data before running one-click, non-interactive, or rm -rf commands. <br>
Risk: Manual cleanup differs by operating system and installation method, so an incorrect command could leave services or files behind. <br>
Mitigation: Follow only the section for the active platform and installation method, then verify that OpenClaw gateway services, scheduled tasks, and CLI packages are removed. <br>


## Reference(s): <br>
- [OpenClaw uninstall documentation](https://docs.openclaw.ai/install/uninstall) <br>
- [OpenClaw GitHub issues](https://github.com/openclaw/openclaw/issues) <br>
- [ClawHub skill page](https://clawhub.ai/dox012/openclaw-uninstaller) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/dox012) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes destructive deletion commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
