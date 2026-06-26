## Description: <br>
Project Memory Ledger helps agents maintain local Markdown engineering ledgers for invariants, decisions, changes, and traceable rollback, with optional Google Drive project-document scaffolding through gws. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zcweah1981](https://clawhub.ai/user/zcweah1981) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve long-running project memory by recording rules, decisions, and changes with evidence and rollback notes. It supports local Markdown ledgers by default and can scaffold project documents in Google Drive when Drive mode is intentionally configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Drive mode can write ledger contents or project documents to Google Workspace. <br>
Mitigation: Use backend=local unless Drive writes are intentional, and verify Drive folder and document IDs before running commands. <br>
Risk: Ledger entries may contain secrets or sensitive internal project notes that could be synced to Drive. <br>
Mitigation: Do not store secrets in ledger entries, and review content before enabling Drive mode or sharing generated documents. <br>
Risk: Incorrect config paths, backend settings, or project IDs can write files or scaffold documents in the wrong workspace. <br>
Mitigation: Start from the bundled default configuration, check paths and IDs, and validate setup with the local backend first. <br>


## Reference(s): <br>
- [Project Memory Ledger on ClawHub](https://clawhub.ai/zcweah1981/project-memory-ledger) <br>
- [README](README.md) <br>
- [Default configuration](references/default_config.json) <br>
- [Ledger templates](references/ledger_templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown ledger entries and files, JSON configuration, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local ledger files; Drive mode can create Google Drive folders and documents through an authenticated gws CLI.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
