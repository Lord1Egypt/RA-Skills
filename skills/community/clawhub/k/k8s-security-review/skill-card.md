## Description:

Analyzes Kubernetes YAML manifests for security misconfigurations, best practices violations, and compliance risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, platform security teams, and Kubernetes administrators use this skill to review Kubernetes YAML manifests before deployment and identify misconfigurations, best-practice violations, and compliance risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kubernetes manifests submitted for review may contain Secrets, tokens, private keys, passwords, registry credentials, sensitive annotations, or internal hostnames.

Mitigation: Redact sensitive values and remove private environment details before submitting manifests to the external review API.

Risk: The release evidence does not provide clear retention, logging, deletion, or privacy commitments for data sent to the external service.

Mitigation: Use the skill only with manifests approved for external processing, or obtain publisher privacy and retention assurances before using production data.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/k8s-security-review)
- [Kubernetes Security Review API Docs](https://api.mkkpro.com:8022/docs)
- [Kubernetes Security Review API Route](https://api.mkkpro.com/security/k8s-security-review)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON security analysis report with findings, severity ratings, recommendations, and summary statistics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include manifest validity, categorized findings, affected resources, remediation recommendations, severity counts, and a compliance score.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
