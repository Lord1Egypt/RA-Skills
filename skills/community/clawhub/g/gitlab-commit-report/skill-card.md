## Description: <br>
GitLab group push events collector and daily commit report generator. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bondli](https://clawhub.ai/user/bondli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and team leads use this skill to collect GitLab group push activity from an authenticated Chrome session and generate daily commit summaries for a configured group. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthorized or overbroad collection of GitLab group activity. <br>
Mitigation: Run the skill only for GitLab groups the user is authorized to monitor, and verify config.json before collection. <br>
Risk: Generated JSON and Markdown reports may contain workplace activity data. <br>
Mitigation: Store generated files in a protected location and periodically delete reports that are no longer needed. <br>
Risk: Cron scheduling can repeatedly collect activity without active review. <br>
Mitigation: Enable cron only after confirming the configured GitLab group, storage location, and reporting need. <br>
Risk: Report date input lacks path validation. <br>
Mitigation: Use report dates in YYYY-MM-DD form until path validation is added. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bondli/gitlab-commit-report) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [JSON data files, Markdown reports, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes dated files under ~/openclaw-skill-data/gitlab-commit-report/; reports can be generated for a supplied YYYY-MM-DD date.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact/package.json declares 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
