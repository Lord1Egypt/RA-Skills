## Description:

Fast TCP port scanner for network reconnaissance and security auditing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and operators use this skill to check open TCP ports, identify common services, and audit exposed attack surface on systems they own or are explicitly authorized to test.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can actively probe arbitrary hosts without explicit authorization safeguards.

Mitigation: Use it only against systems you own or are explicitly authorized to test, and review the target before execution.

Risk: Large port ranges or high worker counts can create operational noise or trigger monitoring.

Mitigation: Start with narrow port selections and conservative worker counts, then expand only when the scan scope is approved.

Risk: Banner grabbing sends traffic to open services and may be logged by the target system.

Mitigation: Disable banner grabbing when service probing is not needed or when the authorization scope does not include active service interrogation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnywang2001/skills/jrv-port-scanner)
- [Publisher profile](https://clawhub.ai/user/johnnywang2001)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands; scanner results are plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scanner accepts a target host, optional ports or top-N selection, timeout, worker count, banner toggle, and output format.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
