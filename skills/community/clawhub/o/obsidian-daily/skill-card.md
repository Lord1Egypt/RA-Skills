## Description: <br>
Manage Obsidian Daily Notes via obsidian-cli by creating and opening daily notes, appending journal entries, logs, tasks, and links, reading past notes by date, and searching vault content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bastos](https://clawhub.ai/user/bastos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage Obsidian daily notes from an agent session, including creating daily files, appending structured entries, reading date-based notes, and searching vault content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vault reads and searches can surface private Obsidian note content to the agent. <br>
Mitigation: Confirm which Obsidian vault is configured as default, and avoid broad searches or reads when the vault contains notes that should not be surfaced. <br>
Risk: Append and create commands can modify daily notes in the configured vault. <br>
Mitigation: Review append and create requests before allowing execution, and install obsidian-cli only from a trusted source. <br>


## Reference(s): <br>
- [Obsidian Daily on ClawHub](https://clawhub.ai/bastos/obsidian-daily) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands assume obsidian-cli is installed and a target Obsidian vault is configured or provided.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
