## Description: <br>
NIST Cybersecurity Framework (CSF) and SP 800-53 Rev 5 compliance assessment for network infrastructure, mapping device configuration against six control families with direct network device relevance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security, compliance, and network engineering teams use this skill to assess network devices against NIST SP 800-53 Rev 5 and CSF 2.0 controls for FISMA, NIST 800-171, CMMC, audit preparation, and security posture baselining. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Assessment outputs can expose sensitive network configuration data, including usernames, IP addresses, AAA server details, SNMP communities, password hashes, and active session information. <br>
Mitigation: Use scoped read-only accounts, define the assessment boundary before collection, and redact raw device outputs before sharing results. <br>
Risk: Running assessment commands against devices without authorization may violate operational or policy boundaries. <br>
Mitigation: Install and use the skill only when authorized to assess the target network devices. <br>


## Reference(s): <br>
- [CLI Reference](references/cli-reference.md) <br>
- [Control Reference](references/control-reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/vahagn-madatyan/nist-compliance-assessment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with read-only CLI command examples and compliance assessment report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on read-only network device assessment; raw device outputs may contain sensitive configuration details that should be redacted before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
