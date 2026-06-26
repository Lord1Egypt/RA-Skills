## Description: <br>
Automatically consolidates daily memories by scoring and filtering entries from MemOS SQLite and daily logs, writing top insights to MEMORY.md each morning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rongtianhua](https://clawhub.ai/user/rongtianhua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain long-term local memory by reviewing daily DREAMS.md drafts, promoting selected entries into MEMORY.md, and auditing memory quality over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated memory consolidation can rewrite persistent memory content when apply mode is used. <br>
Mitigation: Run without --apply first, inspect DREAMS.md, and only apply after confirming promoted entries are useful. <br>
Risk: Weekly audit apply mode can delete memory entries, including orphan entries and high-confidence noise. <br>
Mitigation: Keep MEMORY.md under backup or version control, inspect AUDIT.md, and review the generated backup before relying on cleanup. <br>
Risk: Scheduled cron execution may repeatedly alter local memory files without immediate review. <br>
Mitigation: Verify cron jobs before enabling them and disable or adjust schedules if unattended memory edits are not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rongtianhua/memos-dreaming) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Configuration guidance] <br>
**Output Format:** [Markdown files, console output, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes DREAMS.md and AUDIT.md for review; --apply can update MEMORY.md and local deduplication or audit files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
