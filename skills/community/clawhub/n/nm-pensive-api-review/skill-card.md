## Description:

Evaluates API surface design, consistency, and exemplar alignment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API owners use this skill before releasing public API changes to inventory the surface, compare its conventions with relevant exemplars, and review documentation and versioning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unpinned `npx typedoc` command may download and run third-party code.

Mitigation: Use a pinned, reviewed TypeDoc dependency with a lockfile, and avoid implicit package downloads.

Risk: The security scan is incomplete because three local references could not be resolved.

Mitigation: Resolve and review the missing local references before relying on the skill.

## Reference(s):

- [pandas DataFrame API](https://pandas.pydata.org/docs/reference/frame.html)
- [requests API](https://requests.readthedocs.io/en/latest/api/)
- [Tokio Runtime API](https://docs.rs/tokio/latest/tokio/runtime/)
- [Serde](https://docs.rs/serde/latest/serde/)
- [Go net/http](https://pkg.go.dev/net/http)
- [Go database/sql](https://pkg.go.dev/database/sql)
- [Express 4 API](https://expressjs.com/en/4x/api.html)
- [Stripe API](https://stripe.com/docs/api)
- [GitHub REST API](https://docs.github.com/en/rest)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands]

**Output Format:** [Structured Markdown review with an API inventory, exemplar comparison, evidence-backed findings, and action plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include source locations and quoted anchors for verification.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
