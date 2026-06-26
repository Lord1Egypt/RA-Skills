## Description: <br>
Manage Node.js versions using NVS (Node Version Switcher). Use when switching Node.js versions, installing new versions, managing version aliases, or when the user mentions NVS, node version management, or needs to change the active Node.js version in the current environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuzeyu22](https://clawhub.ai/user/zhuzeyu22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install, switch, list, remove, and troubleshoot Node.js versions with NVS across project environments. It also helps configure aliases, automatic version switching, global package migration, custom remotes, and VS Code integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose commands that clone from GitHub, source shell scripts, or download Node.js builds. <br>
Mitigation: Review each command before execution and confirm the source, path, and target version are appropriate for the environment. <br>
Risk: The skill may propose persistent environment changes such as aliases, default links, or NVS auto-switching. <br>
Mitigation: Require explicit confirmation before applying persistent changes and verify the active Node.js version after the change. <br>
Risk: The skill may propose removing Node.js versions or migrating global npm packages. <br>
Mitigation: Confirm the affected versions and package scope before removal or migration commands are run. <br>


## Reference(s): <br>
- [NVS project repository referenced by the skill](https://github.com/jasongin/nvs) <br>
- [NVS command reference](artifact/REFERENCE.md) <br>
- [NVS usage examples](artifact/EXAMPLES.md) <br>
- [ClawHub skill page](https://clawhub.ai/zhuzeyu22/nvs-node-version-switcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that install NVS, download Node.js versions, change shell environment variables, or set persistent Node.js defaults.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
