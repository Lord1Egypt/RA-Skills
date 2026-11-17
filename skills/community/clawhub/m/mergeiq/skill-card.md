## Description:

Scores GitLab merge requests and GitHub pull requests with a four-dimension complexity framework covering size, cognitive load, review effort, and risk or impact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larryfang](https://clawhub.ai/user/larryfang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to score, triage, and prioritize GitHub PRs or GitLab MRs by complexity before reviews, backlog grooming, or reporting. It helps explain why a change may need deeper review by returning dimension scores, a tier, and a human-readable summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process PR or MR metadata from private repositories when the user chooses to fetch live GitHub or GitLab data.

Mitigation: Use least-privilege GitHub or GitLab tokens and only analyze repository metadata that is approved for this workflow.

Risk: Live API fetching can expose more review metadata than needed for a given scoring task.

Mitigation: Prefer saved JSON input when tighter control over the analyzed data is required.

## Reference(s):

- [GitHub Pulls REST API documentation](https://docs.github.com/en/rest/pulls/pulls)
- [GitLab Merge Requests API documentation](https://docs.gitlab.com/ee/api/merge_requests.html)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON scoring output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scorer returns total and dimension scores, a complexity tier, summary text, tier insight, and review statistics.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
