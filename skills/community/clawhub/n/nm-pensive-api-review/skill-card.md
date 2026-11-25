## Description:

Evaluates API surface design, consistency, and exemplar alignment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inventory public APIs, compare their design with relevant exemplars, and check consistency and documentation before an API release. It produces evidence-linked findings and a recommendation with action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented `npx typedoc` command is unpinned and could download and run an unreviewed package.

Mitigation: Before running it, confirm TypeDoc is expected and pin it to a reviewed version.

Risk: The security scan is partial because three local references could not be resolved, so it does not establish that all behavior was reviewed.

Mitigation: Review the skill instructions and unresolved references before relying on the scan verdict.

## Reference(s):

- [Pensive project homepage (declared metadata link)](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)
- [pandas DataFrame API](https://pandas.pydata.org/docs/reference/frame.html)
- [requests API](https://requests.readthedocs.io/en/latest/api/)
- [Tokio runtime API](https://docs.rs/tokio/latest/tokio/runtime/)
- [Serde API](https://docs.rs/serde/latest/serde/)
- [Go net/http package](https://pkg.go.dev/net/http)
- [Go database/sql package](https://pkg.go.dev/database/sql)
- [Express API](https://expressjs.com/en/4x/api.html)
- [Stripe API](https://stripe.com/docs/api)
- [GitHub REST API](https://docs.github.com/en/rest)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Markdown API review report with structured findings and a JSON findings record]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-specific inventory and exemplar comparisons, evidence-linked findings, and a timed action plan.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
