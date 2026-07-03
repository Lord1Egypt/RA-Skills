## Description: <br>
Launch unpacked Codex Desktop builds with debug ports and optional SSH host autostart using launch_codex_unpacked.sh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivansslo](https://clawhub.ai/user/ivansslo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to launch Codex Desktop from an extracted app.asar with controlled inspect, remote debugging, app path, temporary artifact, user data directory, and SSH host options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package references a powerful local launch_codex_unpacked.sh script that is not included in the artifact. <br>
Mitigation: Inspect and trust the exact script before use, confirm it is executable, and run the skill only from a directory where that script is known. <br>
Risk: Default launch behavior may open inspect and remote debugging ports. <br>
Mitigation: Use the no-inspect or no-remote-debug options unless debugging is required, and run only in a trusted local environment. <br>
Risk: The launcher may install node or npx through Homebrew by default. <br>
Mitigation: Preinstall required tooling or set AUTO_INSTALL_TOOLS=0 when automatic package installation is not acceptable. <br>
Risk: SSH host mode can modify Codex global state and patch an unpacked app bundle. <br>
Mitigation: Use SSH mode only after verifying the target host and preserve or isolate app and user data directories before launch. <br>


## Reference(s): <br>
- [Server-resolved GitHub provenance](https://github.com/ivansslo/codex-web-ui/tree/main/skills/launch-codex-unpacked) <br>
- [ClawHub skill page](https://clawhub.ai/ivansslo/launch-codex-unpacked) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports the app directory, user data directory, final command line, and SSH host mode status after launch.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
