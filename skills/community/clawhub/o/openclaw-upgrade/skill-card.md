## Description: <br>
Helps users upgrade OpenClaw in network environments where GitHub access blocks npm-based updates by using yarn-based install and verification commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyqdq888](https://clawhub.ai/user/hyqdq888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when OpenClaw upgrades fail because servers cannot reliably reach GitHub-hosted dependency sources. It provides yarn install, registry fallback, and post-upgrade checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Upgrade commands can change the active OpenClaw installation and affect existing plugins or custom extensions. <br>
Mitigation: Back up configuration first, consider pinning a known-good version for production systems, and verify OpenClaw plus plugins after the upgrade. <br>
Risk: Registry fallback commands depend on external package registries that may be unavailable or untrusted in some environments. <br>
Mitigation: Use a registry you trust and verify connectivity before installing. <br>
Risk: Broad activation phrases could surface the skill when the user does not intend to perform an upgrade. <br>
Mitigation: Use the skill only after confirming the user intentionally wants to upgrade OpenClaw. <br>


## Reference(s): <br>
- [OpenClaw Upgrade on ClawHub](https://clawhub.ai/hyqdq888/openclaw-upgrade) <br>
- [Yarn Registry](https://registry.yarnpkg.com) <br>
- [npmmirror Registry](https://registry.npmmirror.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may change the installed OpenClaw version and should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
