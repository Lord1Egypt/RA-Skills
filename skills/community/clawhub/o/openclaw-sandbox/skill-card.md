## Description: <br>
OpenClaw 沙盒测试系统 v2.0 helps users test OpenClaw configuration changes with sandbox scripts, backups, rollback guidance, and configuration validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zoopools](https://clawhub.ai/user/Zoopools) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to initialize a sandbox, test configuration changes, and apply validated changes with backup and rollback steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary says the sandbox safety claims are stronger than the scripts support, and some commands can affect a live OpenClaw setup. <br>
Mitigation: Review and edit the scripts before installation or execution; treat apply-config.sh as production-impacting and verify backups before applying changes. <br>
Risk: Environment cleanup and HOME handling may affect the current shell or local OpenClaw state. <br>
Mitigation: Avoid sourcing cleanup-env.sh, remove or replace the hard-coded HOME path before use, and run scripts from a disposable shell session. <br>
Risk: The sandbox gateway may continue running in the background or load plugins that were not intended for the test. <br>
Mitigation: Disable sandbox plugins that are not needed for the test and confirm how to stop the background sandbox gateway after validation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Zoopools/openclaw-sandbox) <br>
- [Verification report](VERIFICATION_REPORT.md) <br>
- [Small change example](examples/小改动示例.md) <br>
- [Large change example](examples/大改动示例.md) <br>
- [Sandbox contamination cases](examples/污染问题案例.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown instructions with shell scripts and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes scripts that create or modify local OpenClaw sandbox and production configuration state.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
