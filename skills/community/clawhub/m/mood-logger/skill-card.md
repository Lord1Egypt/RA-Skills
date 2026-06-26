## Description: <br>
Logs daily mood entries to an Obsidian vault with fixed formatting, mood scores from 1 to 10, tags, optional notes, and weekly mood report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leo-zzl](https://clawhub.ai/user/leo-zzl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and agents use Mood Logger to capture daily emotional check-ins, store them as Markdown journal files, and generate weekly mood summaries from those records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private mood summaries may be included in recurring weekly reporting and sent to a preset WeChat recipient. <br>
Mitigation: Use local logging by default; enable scheduled delivery only after verifying the recipient, previewing the exact report content, and confirming how to disable the scheduled task. <br>
Risk: Mood records are written to a hard-coded Obsidian/iCloud path from the artifact. <br>
Mitigation: Change the vault path to the intended local Obsidian vault before use. <br>


## Reference(s): <br>
- [Mood Logger ClawHub release](https://clawhub.ai/leo-zzl/mood-logger) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Weekly report setup](artifact/WEEKLY_REPORT_SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown files and console text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes mood entries and weekly reports to local files; scheduled delivery is optional.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
