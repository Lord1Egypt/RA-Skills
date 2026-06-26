## Description: <br>
Hermes Memory CN gives an AI assistant a local, Chinese-optimized long-term memory layer for saving, searching, relating, expiring, exporting, and evolving user memories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dream978](https://clawhub.ai/user/dream978) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to give an assistant persistent local memory for preferences, facts, lessons, trading notes, entity relationships, and repeated workflow patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly persists sensitive conversation details in a local memory database. <br>
Mitigation: Enable it only for intended memory use, decide which categories may be saved, and avoid retaining sensitive personal or financial details unless explicitly approved. <br>
Risk: Exported Markdown backups and scheduled memory maintenance can expose or preserve sensitive information beyond the current conversation. <br>
Mitigation: Review exported files and cron jobs, keep the database and backups in user-controlled storage, and remove stale or sensitive entries during maintenance. <br>
Risk: The skill-evolution workflow can turn remembered patterns into draft or promoted skill files. <br>
Mitigation: Treat generated drafts and promote operations as untrusted until the files, paths, and proposed behavior have been inspected and scanned. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dream978/hermes-memory-cn) <br>
- [Installation guide](references/install.md) <br>
- [AGENTS.md integration guide](references/integration.md) <br>
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local memory search results, Markdown exports, entity relationship summaries, and skill draft files.] <br>

## Skill Version(s): <br>
1.4.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
