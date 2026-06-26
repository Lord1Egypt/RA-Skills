## Description: <br>
Installs, updates, authenticates, configures, and directs JetBrains Junie CLI on macOS or Linux while preserving Junie-native project and user configuration patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inertia186](https://clawhub.ai/user/inertia186) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and host agents use this skill to set up JetBrains Junie CLI, manage Junie configuration and authentication, bootstrap a .junie project layout, and hand focused implementation or review work to Junie with clear constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote installer scripts download and execute code locally. <br>
Mitigation: Prefer package-manager installs where practical, review installer use in sensitive environments, and pin versions when repeatability matters. <br>
Risk: Junie tokens and provider API keys can be exposed if persisted carelessly. <br>
Mitigation: Keep credentials in environment variables when possible and ask before writing secrets to durable Junie configuration files. <br>
Risk: Persistent .junie and ~/.junie configuration changes can alter future Junie behavior. <br>
Mitigation: Review config changes before relying on them and merge existing JSON instead of replacing user or project configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/inertia186/junie) <br>
- [JetBrains Junie CLI](https://junie.jetbrains.com/cli) <br>
- [Junie doc notes](references/junie-doc-notes.md) <br>
- [When Junie setup needs headless-terminal](references/headless-terminal-fit.md) <br>
- [Junie macOS/Linux installer](https://junie.jetbrains.com/install.sh) <br>
- [Junie Windows installer](https://junie.jetbrains.com/install.ps1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local .junie configuration files, bootstrap directories, and Junie task briefs when setup or orchestration work is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
