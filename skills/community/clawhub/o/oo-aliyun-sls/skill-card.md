## Description:

Search and read Alibaba Cloud Simple Log Service data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect Alibaba Cloud SLS projects, logstores, time distributions, and matching log entries through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Missing-tool recovery directs the agent to run a downloaded installer, and its source is unverified.

Mitigation: Review setup behavior, install a reviewed fixed CLI version yourself, and require approval for later installation changes. Grant only the SLS read access needed.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Alibaba Cloud Simple Log Service](https://www.alibabacloud.com/product/log-service)
- [SLS request signatures documentation](https://www.alibabacloud.com/help/en/sls/developer-reference/request-signatures)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with shell command examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries and results from read-oriented SLS queries.]

## Skill Version(s):

1.0.4 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
