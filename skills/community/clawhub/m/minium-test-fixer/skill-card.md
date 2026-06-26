## Description: <br>
Minium Test Fixer helps repair Minium test cases by analyzing failure logs and WXML snapshots, identifying better element locators, proposing code edits, and verifying repaired cases locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiziria](https://clawhub.ai/user/yiziria) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and test engineers use this skill to diagnose Minium element-location failures, update Page Object locators, and rerun local tests before reporting a repair as complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may run local Minium tests and PowerShell commands that activate WeChat Developer Tools. <br>
Mitigation: Review commands before execution and use the skill only inside the intended test repository with the expected tools open. <br>
Risk: The workflow may edit project files while repairing locators. <br>
Mitigation: Confirm proposed edits before applying them and verify the repair by rerunning the relevant local test. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yiziria/minium-test-fixer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed file edits, Minium test commands, PowerShell commands for WeChat Developer Tools activation, and local verification results.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
