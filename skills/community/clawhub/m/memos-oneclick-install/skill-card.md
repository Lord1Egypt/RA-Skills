## Description: <br>
Persistent local memory for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mathematics-yang](https://clawhub.ai/user/mathematics-yang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to install, configure, upgrade, and troubleshoot the MemOS local memory plugin. It supports persistent local conversation memory, task summaries, skill evolution, and a local Memory Viewer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill authorizes broad local installation actions, including package installation, OpenClaw configuration changes, gateway restarts, and fallback remote-script execution. <br>
Mitigation: Install only when those local changes are intended; review commands and configuration changes before running them, and prefer verified package-manager installation over pipe-to-shell fallbacks. <br>
Risk: The skill configures persistent local conversation memory that can retain sensitive conversation content. <br>
Mitigation: Review Memory Viewer contents and retention settings before using the plugin with sensitive conversations, and back up or delete the local database according to user policy. <br>
Risk: External embedding providers can require API keys and may send text to third-party services when configured. <br>
Mitigation: Prefer the local embedding option for offline use, and use environment-variable references rather than pasting API keys directly into configuration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mathematics-yang/memos-oneclick-install) <br>
- [MemOS documentation](https://memos-claw.openmem.net/docs/) <br>
- [MemOS plugin npm package](https://www.npmjs.com/package/@memtensor/memos-local-openclaw-plugin) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to modify local OpenClaw configuration, install packages, restart the gateway, and report verification results.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
