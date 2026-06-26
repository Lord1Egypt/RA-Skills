## Description: <br>
Switch AI models without switching tabs using the HokiPoki CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[budjoskop](https://clawhub.ai/user/budjoskop) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to route coding, review, and troubleshooting requests between Claude, Codex, and Gemini through the HokiPoki CLI, including requester workflows and provider/listener mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send selected project files, directories, or broad repository contents to remote AI providers. <br>
Mitigation: Prefer specific files over directories or --all, and avoid sending secrets, regulated data, or other sensitive content. <br>
Risk: Remote patches may be applied to the workspace. <br>
Mitigation: Use --no-auto-apply when appropriate and review diffs before accepting changes. <br>
Risk: Provider/listener mode may expose local AI accounts for remote task execution. <br>
Mitigation: Run provider/listener mode only in trusted workspaces with accounts intended for that purpose. <br>


## Reference(s): <br>
- [HokiPoki CLI Command Reference](references/commands.md) <br>
- [ClawHub HokiPoki Skill Page](https://clawhub.ai/budjoskop/hokipoki) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to request JSON output from the HokiPoki CLI and to review patches before applying them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
