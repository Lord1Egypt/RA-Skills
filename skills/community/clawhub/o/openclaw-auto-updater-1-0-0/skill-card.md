## Description: <br>
Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[q262045312-ui](https://clawhub.ai/user/q262045312-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Clawdbot users use this skill to configure scheduled update checks that update Clawdbot and installed skills, then return a concise summary of what changed or failed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can configure unattended scheduled updates that repeatedly change Clawdbot and installed skills without per-update approval. <br>
Mitigation: Start with dry runs, restrict updates to trusted or pinned sources where possible, and review update summaries after each run. <br>
Risk: A failed or incompatible update could affect the user's Clawdbot installation or installed skills. <br>
Mitigation: Keep rollback steps or backups available, review reported errors, and verify that the cron job can be removed with `clawdbot cron remove "Daily Auto-Update"`. <br>


## Reference(s): <br>
- [Agent Implementation Guide](references/agent-guide.md) <br>
- [Update Summary Examples](references/summary-examples.md) <br>
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating) <br>
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub) <br>
- [Cron Jobs](https://docs.clawd.bot/cron) <br>
- [ClawHub Skill Page](https://clawhub.ai/q262045312-ui/openclaw-auto-updater-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cron schedule, timezone, delivery settings, version summaries, update status, and error notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
