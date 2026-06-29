## Description: <br>
Evaluates API surface design, consistency, and exemplar alignment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API reviewers use this skill before API releases to inventory public surfaces, compare them against high-quality exemplars, audit consistency, and identify documentation or versioning gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect repository documentation and agent-instruction files and may suggest or apply documentation changes during review. <br>
Mitigation: Run in report-only mode when you only want findings, and review proposed documentation changes before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-pensive-api-review) <br>
- [ClawHub metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>
- [pandas DataFrame API reference](https://pandas.pydata.org/docs/reference/frame.html) <br>
- [requests API reference](https://requests.readthedocs.io/en/latest/api/) <br>
- [tokio runtime API reference](https://docs.rs/tokio/latest/tokio/runtime/) <br>
- [serde API reference](https://docs.rs/serde/latest/serde/) <br>
- [Go net/http package reference](https://pkg.go.dev/net/http) <br>
- [Go database/sql package reference](https://pkg.go.dev/database/sql) <br>
- [Express 4.x API reference](https://expressjs.com/en/4x/api.html) <br>
- [Stripe API documentation](https://stripe.com/docs/api) <br>
- [GitHub REST API documentation](https://docs.github.com/en/rest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with command examples and action items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file and line references, API inventory counts, exemplar comparisons, consistency findings, documentation gaps, release recommendation, and timed action plan.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
