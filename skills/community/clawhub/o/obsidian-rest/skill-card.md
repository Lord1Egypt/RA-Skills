## Description: <br>
Read, write, search, append, patch, and manage notes in any Obsidian vault via the Local REST API on Windows, macOS, or Linux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nj070574-gif](https://clawhub.ai/user/nj070574-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Obsidian users use this skill to let an agent read, search, create, append, patch, delete, and summarize vault notes through the Obsidian Local REST API plugin. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent API-key access to read and modify an Obsidian vault. <br>
Mitigation: Install only for vaults where agent access is acceptable, protect the API key, and avoid exposing the REST API beyond trusted local networks. <br>
Risk: Overwrite, delete, patch, and command-execution actions can change vault contents or Obsidian state. <br>
Mitigation: Require confirmation before overwrites, deletes, patches, or command execution, and prefer reading the current note before modifying it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nj070574-gif/obsidian-rest) <br>
- [Obsidian Local REST API plugin](https://github.com/coddingtonbear/obsidian-local-rest-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text with curl and bash command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interprets API responses in plain English and may create, append, patch, delete, or summarize Obsidian notes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
