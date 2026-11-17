## Description:

Nist Compliance Assessment helps agents assess network infrastructure against NIST CSF and SP 800-53 Rev 5 controls using read-only device configuration and operational checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Security and compliance engineers use this skill to scope network device assessments, map device configuration and operational state to NIST CSF and SP 800-53 controls, and produce gap analysis for FISMA, CMMC, FedRAMP, and enterprise posture reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthorized assessment or collection of sensitive network device data.

Mitigation: Use the skill only with explicit authorization and treat account listings, SNMP settings, ACLs, and software versions as sensitive operational data.

Risk: Incorrect compliance conclusions if the assessment boundary or FIPS 199 impact level is missing.

Mitigation: Confirm the authorization boundary and Low, Moderate, or High impact categorization before interpreting control gaps.

## Reference(s):

- [NIST 800-53 Compliance CLI Reference](references/cli-reference.md)
- [NIST 800-53 Rev 5 Control Reference - Network Device Mapping](references/control-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown assessment guidance with read-only CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include compliance findings, control gap analysis, and POA&M guidance; collected device outputs should be handled as sensitive operational data.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
