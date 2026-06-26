## Description: <br>
Evaluates API surface design, consistency, and exemplar alignment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API maintainers use this skill to review public API changes, design new API surfaces, audit consistency, and validate documentation completeness before release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation keywords may cause the skill to run during unrelated documentation or design conversations. <br>
Mitigation: Invoke it explicitly for public API reviews or release checks and confirm the intended review scope before applying recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-pensive-api-review) <br>
- [Pensive plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>
- [pandas DataFrame API](https://pandas.pydata.org/docs/reference/frame.html) <br>
- [requests API](https://requests.readthedocs.io/en/latest/api/) <br>
- [tokio runtime API](https://docs.rs/tokio/latest/tokio/runtime/) <br>
- [serde API](https://docs.rs/serde/latest/serde/) <br>
- [Go net/http package](https://pkg.go.dev/net/http) <br>
- [Express 4.x API](https://expressjs.com/en/4x/api.html) <br>
- [Stripe API documentation](https://stripe.com/docs/api) <br>
- [GitHub REST API documentation](https://docs.github.com/en/rest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with command evidence, file and line references, issue findings, release recommendation, and timed action plan] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API surface inventory, exemplar alignment, consistency gaps, documentation gaps, and an approve/block recommendation.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
