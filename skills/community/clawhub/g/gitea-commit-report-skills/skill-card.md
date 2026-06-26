## Description: <br>
Collects Gitea repository commit activity, uses AI to summarize project progress, and helps send HTML progress reports to repository administrators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and team leads use this skill to generate daily, weekly, or ad hoc progress reports from Gitea repositories over a selected date range. It can cover all repositories visible to the configured token or a specified owner/repo, then prepare HTML email reports for repository administrators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can gather activity across all repositories visible to the configured Gitea token and email generated reports to derived recipients. <br>
Mitigation: Use a read-only, narrowly scoped Gitea token; prefer a single repository and date range when practical; confirm the recipient list, report preview, and GITEA_URL before allowing email to be sent. <br>
Risk: AI-generated summaries and risk notes may be incomplete or misleading when included in progress-report emails. <br>
Mitigation: Review the generated JSON summary and HTML report preview before sending externally or using the report for management decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/myd2002/gitea-commit-report-skills) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/myd2002) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON fields; generated report emails are HTML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GITEA_URL and GITEA_TOKEN; can operate on all visible repositories or a specified owner/repo and date range.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
