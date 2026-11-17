## Description:

Detects the LiteLLM supply chain attack (v1.82.7/1.82.8) by scanning for compromised packages, malicious .pth files, backdoor persistence, suspicious network connections, and Kubernetes IoCs in a read-only, dependency-free workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjefferson](https://clawhub.ai/user/tjefferson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security teams, and incident responders use this skill to run a read-only LiteLLM compromise detector for known supply-chain attack indicators in local Python, network, and Kubernetes environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The detector may issue DNS queries for known indicator domains during execution.

Mitigation: Run it knowingly in sensitive or air-gapped environments, and account for those DNS lookups in monitoring or change records.

Risk: When kubectl is available, the detector may use the current Kubernetes context for read-only cluster checks.

Mitigation: Confirm the active kubectl context before running, or run without kubectl access if cluster inspection is not intended.

Risk: The tool is scoped to known LiteLLM 1.82.7 and 1.82.8 compromise indicators and may not detect unrelated threats.

Mitigation: Use results as one incident-response signal and continue normal host, credential, cloud, and Kubernetes review when compromise is suspected.

## Reference(s):

- [LiteLLM issue 24512](https://github.com/BerriAI/litellm/issues/24512)
- [Original check-litellm script](https://gist.github.com/sorrycc/30a765b9a82d0d8958e756b251828a19#file-check-litellm-sh)

## Skill Output:

**Output Type(s):** [Shell commands, Analysis, Guidance]

**Output Format:** [Markdown guidance with bash command and terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only detector output uses color-coded status markers and exit code 0 or 1.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
