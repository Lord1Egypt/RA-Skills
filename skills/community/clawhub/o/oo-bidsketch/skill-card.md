## Description:

Searches and reads BidSketch client and proposal data through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and account operators use this skill to find clients, retrieve proposal details, and review proposal content in BidSketch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback executes remote installers whose behavior has not been verified.

Mitigation: Review and install the CLI yourself, prefer a pinned and verified release, and require approval for setup changes.

Risk: Connecting BidSketch allows OOMOL-mediated access to business records.

Mitigation: Connect an account authorized for this use and limit requests to the records needed for the task.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [BidSketch API documentation](https://github.com/Bidsketch/bidsketch-api)
- [BidSketch](https://www.bidsketch.com/)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured BidSketch records and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only client and proposal results]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
