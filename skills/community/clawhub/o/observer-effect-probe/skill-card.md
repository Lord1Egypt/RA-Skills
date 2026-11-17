## Description:

Helps detect skills that behave differently when they sense they are being monitored, catching attestation and sandbox evasion behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use this skill to probe other agent skills for behavior changes across sandbox, timing, observer API, and environment variations that may indicate attestation evasion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Probing target skills in production or credentialed environments could expose sensitive systems during repeated environment variation.

Mitigation: Run probes only in isolated sandboxes without real credentials or production access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/skills/observer-effect-probe)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown probe report with scored findings and a verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sandbox fingerprint indicators, invocation sensitivity, observer API inventory, behavioral consistency matrix, evasion probability score, and probe verdict.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
