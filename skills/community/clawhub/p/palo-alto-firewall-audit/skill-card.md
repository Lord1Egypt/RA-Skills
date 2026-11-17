## Description:

PAN-OS zone-based security policy audit with App-ID/Content-ID analysis, Security Profile Group validation, zone protection assessment, and decryption policy review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Network security engineers and firewall administrators use this skill to audit Palo Alto Networks PAN-OS security policies, App-ID coverage, Security Profile Group bindings, zone protection, and decryption posture. It supports rule-level review for PA-series, VM-series, and Panorama-managed deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Firewall API credentials or sensitive audit data may be exposed in shared logs, transcripts, copied URLs, or shell history.

Mitigation: Use a dedicated read-only API account, keep PAN_API_KEY out of shared logs and transcripts, and avoid placing passwords or API keys in URLs or command history.

Risk: Firewall logs, URL data, and WildFire or PAN-DB related data can contain information subject to organizational privacy and compliance requirements.

Mitigation: Review the organization's data-handling rules before collecting or sharing audit output, especially for URL, traffic, threat, and sandbox-related evidence.

## Reference(s):

- [PAN-OS CLI and API Reference](artifact/references/cli-reference.md)
- [PAN-OS Security Policy Evaluation Chain](artifact/references/policy-model.md)
- [ClawHub Release Page](https://clawhub.ai/vahagn-madatyan/skills/palo-alto-firewall-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown audit report and remediation guidance with inline PAN-OS CLI and API commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires read-only PAN-OS or Panorama access; API-backed workflows require PAN_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
