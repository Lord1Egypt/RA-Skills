## Description: <br>
This skill helps agents install, configure, verify, and use memory-lancedb-pro, a long-term memory plugin for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Darcy-Wang](https://clawhub.ai/user/Darcy-Wang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up memory-lancedb-pro, choose a deployment plan, update OpenClaw memory configuration, verify provider keys, and run post-install smoke tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask users to provide raw API keys during setup. <br>
Mitigation: Prefer environment variables or a secret manager, and avoid pasting long-lived keys into chat. <br>
Risk: The skill recommends a remote installer that may be unpinned. <br>
Mitigation: Pin and review the installer source before running it, or use a reviewed manual installation path. <br>
Risk: Configuration changes and gateway restarts can affect an existing OpenClaw deployment. <br>
Mitigation: Ask for a config diff before writes or restarts, validate the config, and keep changes scoped to the memory plugin section. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Darcy-Wang/memory-lancedb-pro-skill) <br>
- [README](README.md) <br>
- [Full technical reference](references/full-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include provider API checks, OpenClaw configuration diffs, restart steps, and smoke-test instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
