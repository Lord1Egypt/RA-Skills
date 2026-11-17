## Description:

Queries pending repurchase, purchase, loss-item, and replenishment records with pagination, status, and sorting parameters through a protected business HTTPS API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kunxinian](https://clawhub.ai/user/kunxinian)

### License/Terms of Use:

MIT-0

## Use Case:

Business operations users invoke this skill to look up pending repurchase or loss-item records and receive a concise natural-language summary of the returned records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses LOSS_API_TOKEN to query internal business records.

Mitigation: Install only for trusted publishers and intended users; use a read-only, narrowly scoped token where possible.

Risk: Broad trigger phrases such as pending or page-number requests may accidentally fetch business records.

Mitigation: Review and tighten activation phrases before deployment in shared or high-sensitivity environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kunxinian/skills/loss-items-query-ailifeassistant)
- [Publisher Profile](https://clawhub.ai/user/kunxinian)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Natural-language summary of JSON records returned by a Python command-line helper.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the LOSS_API_TOKEN environment variable.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
