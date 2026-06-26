## Description: <br>
Handsfree Windows Control guides agents in automating native Windows apps through UIA and web browsers through Playwright via the handsfree-windows CLI, including app launch, control discovery, clicking, typing, browser snapshots, and mixed desktop/web YAML macros. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijinlar](https://clawhub.ai/user/lijinlar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, QA engineers, and automation agents use this skill to control Windows desktop applications and browser sessions for testing, repetitive workflows, and mixed desktop/web automation while discovering UI controls before acting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow installs mutable external code before the CLI is used. <br>
Mitigation: Review or pin the external handsfree-windows repository before running setup. <br>
Risk: The skill can control local Windows applications and websites. <br>
Mitigation: Require explicit human confirmation before send, delete, purchase, posting, account, or business-data actions. <br>
Risk: Browser automation reuses persistent profiles that may retain cookies and login sessions. <br>
Mitigation: Use test accounts or dedicated browser profiles and delete ~/.handsfree-windows/browser-profiles after sensitive work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lijinlar/handsfree-windows-control) <br>
- [handsfree-windows CLI reference](references/api_reference.md) <br>
- [External handsfree-windows CLI repository installed by setup](https://github.com/lijinlar/handsfree-windows.git) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline PowerShell, YAML, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce automation macros and local setup commands; browser workflows can rely on persistent profiles.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
