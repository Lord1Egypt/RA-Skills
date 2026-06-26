## Description: <br>
Triage open PRs by detecting duplicates, assessing quality, and generating prioritized reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zerone0x](https://clawhub.ai/user/zerone0x) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and repository maintainers use Pr Triage to analyze open pull requests, surface likely duplicate work, grade basic readiness signals, and produce a prioritized Markdown report for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use the locally logged-in GitHub CLI account to access pull request metadata. <br>
Mitigation: Confirm the active GitHub account and target repository before running the skill. <br>
Risk: Optional action mode can mutate pull requests by adding comments or labels. <br>
Mitigation: Use report-only mode first, then enable actions only after reviewing the exact comments and labels that will be applied. <br>
Risk: Duplicate and quality scores are heuristic and may produce incorrect recommendations. <br>
Mitigation: Treat the report as triage guidance and have maintainers review recommendations before closing, merging, commenting on, or labeling PRs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zerone0x/pr-triage) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with PR summaries, duplicate groups, quality grades, stale PRs, and review recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May print to stdout or write the report to a user-specified file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
