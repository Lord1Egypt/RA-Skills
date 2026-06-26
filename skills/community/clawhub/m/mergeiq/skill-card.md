## Description: <br>
Scores GitLab merge requests and GitHub pull requests with a four-dimension complexity framework covering size, cognitive load, review effort, and risk/impact. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larryfang](https://clawhub.ai/user/larryfang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to score, triage, and prioritize GitHub PRs or GitLab MRs by review complexity. It helps identify changes that may need deeper review, second reviewers, or team-level complexity reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private PR/MR metadata or fetched JSON may contain sensitive repository details. <br>
Mitigation: Handle fetched JSON as confidential, avoid saving or sharing private repository data unless needed, and follow the security guidance from the release evidence. <br>
Risk: GitHub or GitLab tokens may be needed to fetch private repository data. <br>
Mitigation: Use least-privilege read-only tokens from environment variables or a secure credential manager, and do not hard-code credentials. <br>
Risk: Complexity scores are heuristic and may not reflect every review risk. <br>
Mitigation: Use the score and dimension breakdown as a triage aid, and have reviewers check the underlying change before applying review policy decisions. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/larryfang/mergeiq) <br>
- [GitHub REST API pull requests documentation](https://docs.github.com/en/rest/pulls/pulls) <br>
- [GitLab merge requests API documentation](https://docs.gitlab.com/ee/api/merge_requests.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON with human-readable score summaries and optional Markdown or shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Complexity output includes a total score, tier, four dimension scores, summary, tier insight, and PR/MR statistics.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
