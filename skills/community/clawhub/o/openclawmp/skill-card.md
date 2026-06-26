## Description: <br>
OpenClawMP guides agents through OpenClaw Marketplace registration, authentication, asset discovery, installation, publishing, account management, and community operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[502399493zjw-lgtm](https://clawhub.ai/user/502399493zjw-lgtm) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, agent operators, and marketplace maintainers use this skill to let an agent work with OpenClaw Marketplace assets and accounts through documented CLI and API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Marketplace operations can change local agent installs and account state. <br>
Mitigation: Require explicit user confirmation before install, publish, comment, unbind, uninstall, or delete-account actions. <br>
Risk: Credentials and API keys may be used by CLI or API workflows. <br>
Mitigation: Keep API keys private, prefer environment variables or the documented credentials file, and avoid printing secrets in logs or responses. <br>
Risk: Downloaded marketplace assets may affect future agent sessions after installation. <br>
Mitigation: Review downloaded files and scan installed assets before loading them into an agent runtime. <br>
Risk: The security summary flags unsafe command and path handling in the CLI. <br>
Mitigation: Avoid automatic global updates and review command arguments, paths, and downloaded archives before execution. <br>


## Reference(s): <br>
- [OpenClawMP ClawHub listing](https://clawhub.ai/502399493zjw-lgtm/openclawmp) <br>
- [OpenClaw Marketplace](https://openclawmp.cc) <br>
- [API Reference](references/api.md) <br>
- [Asset Types](references/asset-types.md) <br>
- [OpenClaw Marketplace CLI README](scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to run marketplace CLI commands that read or write local configuration, installed assets, and account state.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
