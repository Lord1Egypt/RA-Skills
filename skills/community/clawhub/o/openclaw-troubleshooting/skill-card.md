## Description: <br>
OpenClaw常见问题解决方案技能，提供自动化诊断、错误修复和性能优化功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[playgod2023](https://clawhub.ai/user/playgod2023) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and skill developers use this skill to diagnose local environment, dependency, workspace, and permission issues and to repair common setup problems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repair mode can change the local Python environment by installing missing packages. <br>
Mitigation: Review the dependency list first and run installs manually in a disposable or backed-up environment when possible. <br>
Risk: Permission repair can apply broad chmod -R 755 changes to the OpenClaw workspace. <br>
Mitigation: Back up important workspaces and prefer manual permission fixes for only the affected paths. <br>
Risk: The quick start and fix all flows can combine dependency, workspace, and permission repairs in one run. <br>
Mitigation: Run diagnostic mode first, then execute only the specific repair action that is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/playgod2023/openclaw-troubleshooting) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Configuration](artifact/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute local Python diagnostics and repair actions when invoked through the included scripts.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
