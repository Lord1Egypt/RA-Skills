## Description: <br>
Automates collection, structuring, search, review, and optional notification workflows for writing external content into an Obsidian inbox. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hunanjsd](https://clawhub.ai/user/hunanjsd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to capture external feeds, articles, and radar outputs into an Obsidian vault, then search or review the resulting inbox notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and write sensitive Obsidian vault content. <br>
Mitigation: Review the configured vault path and run capture or review commands with dry-run or test content before pointing the skill at a personal or production vault. <br>
Risk: The daily pipeline can run code from sibling radar skills outside the reviewed artifact. <br>
Mitigation: Inspect and approve each referenced radar skill before enabling cron or daily automation. <br>
Risk: Optional Telegram and Feishu integrations can send vault-derived content to external services. <br>
Mitigation: Enable notification credentials only after confirming what content will be sent and which recipient IDs are configured. <br>
Risk: Optional index rebuilding can execute a vault-local Node.js script. <br>
Mitigation: Review the vault's rebuild_index.mjs script before enabling automated index rebuilds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hunanjsd/obsidian-inbox-pipeline) <br>
- [Publisher profile](https://clawhub.ai/user/hunanjsd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes, Markdown reports, command-line text, shell commands, and environment-variable configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes Markdown files into an Obsidian vault and can optionally send Telegram or Feishu notifications when configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
