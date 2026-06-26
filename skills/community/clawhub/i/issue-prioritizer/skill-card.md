## Description: <br>
Prioritizes GitHub issues by ROI, solution sanity, and architectural impact to identify quick wins, over-engineered proposals, and actionable bugs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Glucksberg](https://clawhub.ai/user/Glucksberg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and repository maintainers use this skill to triage open GitHub issues, rank them by adjusted priority, identify quick wins, and avoid duplicating work already covered by open pull requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs under the user's authenticated GitHub CLI session and may access repositories available to that account. <br>
Mitigation: Use a fine-grained or read-only GitHub token and avoid running the skill against sensitive private issue trackers unless that access is intended. <br>
Risk: The allowed GitHub command surface is broader than a read-only issue analyzer needs. <br>
Mitigation: Prefer narrowing allowed commands to read-only issue and pull request operations such as `gh issue list/view` and `gh pr list/view`. <br>


## Reference(s): <br>
- [Issue Prioritizer on ClawHub](https://clawhub.ai/Glucksberg/issue-prioritizer) <br>
- [GitHub CLI](https://cli.github.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with issue rankings, category summaries, recommendations, and optional JSON or Markdown table output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only GitHub issue and pull request analysis using an authenticated gh CLI session.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
