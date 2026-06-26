## Description: <br>
Index and search code repositories, documentation, research papers, HuggingFace datasets, local folders, and packages with Nia AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arlanrakh](https://clawhub.ai/user/arlanrakh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI agents use Nia to index, search, and retrieve current context from repositories, documentation, research papers, datasets, packages, local folders, and saved contexts for code research and advisory workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send selected project files, manifests, saved context, and possible database credentials or query data to Nia. <br>
Mitigation: Avoid indexing folders with secrets, use least-privilege read-only database credentials, and review selected files or queries before create, sync, from-db, preview-db, advisor, deps, or context-save commands. <br>
Risk: The API key is stored in a local file and used as a bearer token for Nia API requests. <br>
Mitigation: Protect ~/.config/nia/api_key, rotate it if exposed, and avoid committing or sharing the key file. <br>
Risk: Destructive or state-changing commands can delete, rename, sync, or upload indexed sources and contexts. <br>
Mitigation: Require explicit user approval before delete, rename, sync, upload, subscribe, or indexing commands that change remote Nia state. <br>


## Reference(s): <br>
- [Nia Skill on ClawHub](https://clawhub.ai/arlanrakh/nia) <br>
- [Nia Homepage](https://trynia.ai) <br>
- [Nia Documentation](https://docs.trynia.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON responses from shell scripts, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return search results, file excerpts, repository trees, research summaries, dependency analysis, and code advice depending on the selected Nia script.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
