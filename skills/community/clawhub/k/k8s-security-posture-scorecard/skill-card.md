## Description:

Assesses Kubernetes cluster security posture across 30 controls covering RBAC, workload security, network policies, IaC, runtime monitoring, and secrets management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps teams, SREs, and security engineers use this skill to collect Kubernetes control answers, call the ToolWeb scorecard API, and present a cluster security score, domain grades, critical findings, and prioritized remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kubernetes security posture details are sent to ToolWeb.in for scoring.

Mitigation: Confirm organizational approval for third-party processing, use aliases instead of real cluster names, and avoid secrets, internal hostnames, or sensitive notes.

Risk: Successful API calls may consume ToolWeb quota or create billing activity.

Mitigation: Confirm the active ToolWeb subscription and expected usage before running assessments, especially repeated or automated assessments.

Risk: The skill depends on an external API and instructs the agent not to create a local fallback scorecard if the API fails.

Mitigation: Report API failures clearly, retry only when appropriate, and use an approved internal assessment process when offline scoring is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/k8s-security-posture-scorecard)
- [ToolWeb Platform](https://toolweb.in)
- [ToolWeb API Portal](https://portal.toolweb.in)
- [Kubernetes Scorecard API Endpoint](https://portal.toolweb.in/apis/security/k8scorecard)
- [ToolWeb MCP Server](https://hub.toolweb.in)
- [ToolWeb OpenClaw Skills](https://toolweb.in/openclaw/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown scorecard with domain scores, critical findings, warnings, and a prioritized remediation roadmap.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; successful API calls may consume ToolWeb quota or incur billing.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
