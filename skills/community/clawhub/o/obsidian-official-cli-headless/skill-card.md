## Description: <br>
Installs and adapts the official Obsidian CLI for headless Linux servers using a dedicated non-root user, Xvfb, ACL-based vault access, and an obs wrapper command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DarinRowe](https://clawhub.ai/user/DarinRowe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up the official Obsidian CLI on Debian or Ubuntu-like headless servers where root execution, missing display sessions, or vault permissions would otherwise prevent reliable CLI use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup performs persistent root-level system changes, including package installation, user creation, wrapper installation, and ACL updates. <br>
Mitigation: Run it only on machines where those changes are acceptable, review the scripts before execution, and prefer an isolated host or fresh environment. <br>
Risk: Weak path guardrails could broaden access if an unsafe vault path or wrapper path is supplied. <br>
Mitigation: Use a dedicated vault path, avoid broad paths such as /, /root, /home, or application directories, and set WRAPPER_PATH only after auditing the destination. <br>
Risk: Verification writes a marker into the selected vault. <br>
Mitigation: Run verification against a fresh or disposable vault when possible, or remove the verification marker after confirming behavior. <br>


## Reference(s): <br>
- [Architecture notes](references/architecture.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [ClawHub release page](https://clawhub.ai/DarinRowe/obsidian-official-cli-headless) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports the installed version, wrapper path, active vault path, verified commands, and remaining limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
