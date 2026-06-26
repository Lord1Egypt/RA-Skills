## Description: <br>
A beginner-friendly OpenClaw learning pack that introduces ten core agent tools for file operations, search, shell execution, messaging, sub-agents, and Git workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tpc1009](https://clawhub.ai/user/tpc1009) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this pack to learn common OpenClaw tool patterns, including reading and writing files, searching text, running shell commands, asking users questions, sending messages, delegating work to sub-agents, and using Git-aware workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The pack exposes beginner users to powerful file, shell, messaging, and Git actions that can change a workspace or send information outside the current task. <br>
Mitigation: Review the pack before installing it in real projects, do not paste passwords, tokens, or API keys into chat, and verify message destinations before sending information externally. <br>
Risk: The Git-aware workflow includes automatic commit behavior that can capture unintended changes if the diff and staged files are not reviewed first. <br>
Mitigation: Inspect the diff and explicitly decide which files should be staged before using the auto-commit helper. <br>


## Reference(s): <br>
- [ClawHub Learning Pack](https://clawhub.ai/tpc1009/learning-pack) <br>
- [Aider Git Integration](https://github.com/Aider-AI/aider) <br>
- [Conventional Commits](https://www.conventionalcommits.org/) <br>
- [Atlassian Git Workflows](https://www.atlassian.com/git/tutorials/comparing-workflows) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, YAML examples, and concise tool usage notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the selected tool skill and may include workspace file changes, command output, user prompts, or Git workflow guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
