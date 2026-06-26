## Description: <br>
Hermes Memory Bridge connects Hermes Agent and WorkBuddy so agents can sync memories, exchange signal events, and process closed-loop task commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuboacean](https://clawhub.ai/user/liuboacean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to bridge Hermes Agent and WorkBuddy memories, signals, queues, and task feedback. It is intended for users who deliberately want persistent local coordination between the two agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge gives a persistent background process authority over shared memories, task commands, and feedback files. <br>
Mitigation: Install only when that cross-agent authority is intentional, restrict shared-directory permissions, and require manual approval or an allowlist for task changes, memory writes, and commands from shared signal files. <br>
Risk: Shared memory and feedback files can expose or overwrite personal agent context. <br>
Mitigation: Back up Hermes and WorkBuddy memory files before enabling the watcher, and review write paths and retention settings before running it continuously. <br>
Risk: Optional extensions can broaden the command surface beyond memory synchronization. <br>
Mitigation: Remove or disable unneeded extensions such as weather handling and keep only the commands required for the deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liuboacean/hermes-memory-bridge) <br>
- [Publisher Profile](https://clawhub.ai/user/liuboacean) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets, plus JSON signal and task payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local file-based bridge operations and command guidance; no multimedia output.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
