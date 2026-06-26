## Description: <br>
Audits merged GitCode pull requests across one or more repositories for labels, comments, tests, size, issue linkage, review coverage, and title or description clarity, then outputs a Markdown or CSV table. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autoxj](https://clawhub.ai/user/autoxj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering maintainers use this skill to sample or check merged GitCode PRs across repositories and produce PR compliance summaries for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad or over-privileged GITCODE_TOKEN could expose more repository metadata than the audit requires. <br>
Mitigation: Use a read-only or least-privilege GitCode token scoped to the repositories being audited. <br>
Risk: Large repo/date ranges or --all can collect many PR titles, links, labels, comments, and review details. <br>
Mitigation: Review repository and date-range inputs before execution, especially before using --all. <br>
Risk: Optional report files may persist internal PR metadata on disk. <br>
Mitigation: Choose --output paths carefully and handle generated Markdown or CSV reports according to internal data-handling policy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/autoxj/gitcode-pr-audit) <br>
- [GitCode personal access token settings](https://gitcode.com/setting/token-classic) <br>
- [GitCode API base](https://api.gitcode.com/api/v5) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown table on stdout, with optional Markdown or CSV report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GITCODE_TOKEN and at least one owner/repo target; reports may include PR titles, links, labels, comments, and review details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
