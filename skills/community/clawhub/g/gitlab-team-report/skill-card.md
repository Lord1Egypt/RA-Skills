## Description: <br>
Generates GitLab weekly team reports with merge request categorization, contributor and repository summaries, Markdown and HTML output, charts, historical report index pages, and optional Feishu publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzn](https://clawhub.ai/user/wangzn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering managers use this skill to summarize GitLab merge requests, commits, contributors, repositories, and product-area work for recurring team reports and stakeholder updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A GitLab token and Feishu credentials may expose private repository activity or documents if stored or shared carelessly. <br>
Mitigation: Use least-privilege tokens, keep local configuration files private, and do not publish real tokens or private config values. <br>
Risk: Recurring cron execution can automatically generate and upload reports without a fresh per-run review. <br>
Mitigation: Run setup-cron.sh only when recurring Feishu publication is intended, and review the generated schedule and log path before enabling it. <br>
Risk: Uploading with an existing Feishu document URL can overwrite document contents. <br>
Mitigation: Prefer creating a new Feishu document, or confirm that overwriting the existing document is acceptable before passing a document URL. <br>
Risk: Generated reports may include sensitive team activity, repository names, links, or contribution details. <br>
Mitigation: Inspect weekly_report.md and weekly_report.html before sharing or uploading them outside the intended audience. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangzn/gitlab-team-report) <br>
- [GitLab API endpoint configured by users](https://gitlab.example.com) <br>
- [Feishu Open Platform API](https://open.feishu.cn/open-apis) <br>
- [Feishu document publishing target](https://feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and HTML reports, JSON statistics, chart files or Mermaid chart Markdown, shell commands, and configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are written under a configured reports directory and may be published to Feishu when explicitly configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
