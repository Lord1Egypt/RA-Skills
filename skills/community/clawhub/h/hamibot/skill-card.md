## Description: <br>
Hamibot helps agents work with the Hamibot CLI, an open-source Node.js command-line tool for authorized remote Android automation on paired user devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hamibot](https://clawhub.ai/user/hamibot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install, authenticate, and operate the Hamibot CLI for authorized automation of their own paired Android devices. Typical tasks include code execution, file management, input simulation, screenshots, app launch, and device queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can run code, simulate input, manage files, capture screenshots, and launch apps on paired Android devices. <br>
Mitigation: Use it only with devices the user owns or is explicitly authorized to administer, and review commands and scripts before execution. <br>
Risk: Authentication through interactive login or a Personal Access Token can grant access to the user's paired devices. <br>
Mitigation: Protect tokens and credentials, avoid sharing them in prompts or logs, and revoke or rotate tokens when no longer needed. <br>
Risk: The bundled security evidence was clean but noted that full artifact coherence review was limited. <br>
Mitigation: Inspect the visible skill instructions and install steps before use, especially before global npm installation or persistent automation workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hamibot/hamibot) <br>
- [Hamibot Official Site](https://hamibot.com) <br>
- [Hamibot CLI Repository](https://github.com/hamibot/cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and command reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that install the CLI, authenticate, select devices, execute code, manage files, simulate input, capture screenshots, launch apps, and query device information.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
