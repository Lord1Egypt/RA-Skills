## Description: <br>
本地长记忆 is a local vector-memory skill that helps agents store, retrieve, and maintain semantic memory with Ollama embeddings, LanceDB storage, cache controls, and offline operation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent operators, and privacy-sensitive teams use this skill to add local long-term memory to agents, especially for offline workflows, regulated data handling, personal knowledge bases, and low-cost semantic recall. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive user, business, medical, financial, or legal details in local long-term memory. <br>
Mitigation: Define consent, retention, and never-store rules before enabling memory capture, and avoid storing sensitive data unless the local environment is approved for it. <br>
Risk: Local memory directories and vector databases can expose private history if the workspace or machine is shared, backed up insecurely, or compromised. <br>
Mitigation: Restrict filesystem access to the memory directory, protect backups, and align local storage with the user's security requirements. <br>
Risk: Forget, cleanup, compact, and dedup maintenance commands can remove or transform stored memory. <br>
Mitigation: Create a backup before running destructive or bulk maintenance commands and review the intended query or retention window. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/localmemo-pro) <br>
- [Ollama installation](https://ollama.com/install) <br>
- [Ollama download](https://ollama.com/download) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup, memory store/search/forget, maintenance, backup, and local configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
