## Description: <br>
Jira Issue Analyzer fetches Jira issue details and attachments, delegates evidence-driven log analysis, and produces a local Markdown issue analysis report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dimos92](https://clawhub.ai/user/dimos92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support engineers use this skill to collect Jira issue data and attachments, analyze logs and related evidence, and create a structured Markdown report for issue triage and root-cause investigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Jira token to fetch issue data and attachments. <br>
Mitigation: Use a least-privilege Jira token and keep the .env file out of source control. <br>
Risk: Attachment handling can write files outside the intended folder when attachment names are unsafe. <br>
Mitigation: Run the skill in an isolated working directory and review or patch attachment filename handling before processing untrusted attachments. <br>
Risk: ZIP extraction and downloaded attachments may contain untrusted files. <br>
Mitigation: Inspect attachments before opening or executing them, and patch ZIP extraction handling before use on tickets with untrusted attachments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dimos92/jira-issue-analyzer) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Jira script usage](artifact/jira/README.md) <br>
- [Report template](artifact/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with supporting command-line output and JSON issue data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are intended to be saved locally under a project Jira work directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
