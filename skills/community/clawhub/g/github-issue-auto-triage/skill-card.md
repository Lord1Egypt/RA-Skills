## Description: <br>
Automatically triages GitHub issues by classifying new issues, applying labels, detecting likely duplicates, and posting FAQ-style replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository maintainers use this skill to review unclassified GitHub issues, preview triage behavior in dry-run mode, and apply labels or FAQ replies in configured repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live changes to GitHub issues, including labels and comments. <br>
Mitigation: Run dry-run first and use a fine-grained GitHub token limited to the intended repository and issue permissions. <br>
Risk: Issue titles and body text may be sent to DashScope for classification. <br>
Mitigation: Avoid private or security-sensitive issues unless the repository owner accepts that third-party LLM data flow. <br>
Risk: Scheduled execution can repeatedly act on issues before behavior is validated. <br>
Mitigation: Validate manually on a small repository or issue subset before enabling cron or other recurring automation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/SxLiuYu/github-issue-auto-triage) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [TEST-REPORT.md](artifact/TEST-REPORT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, console logs, and JSON triage reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform GitHub API mutations and may write timestamped triage_results JSON files when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
