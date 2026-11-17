## Description:

Screens medical-device classification and likely registration routes for China, the EU, and the US, returning preliminary JSON guidance for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT (Python code only); skill and documentation text all rights reserved

## Use Case:

Medical-device developers and regulatory teams use this skill to triage a device's likely risk class and registration pathway before preparing filings. Results are preliminary and require review against current official rules or qualified counsel.

### Deployment Geography for Use:

China, European Union, and United States (screening coverage)

## Known Risks and Mitigations:

Risk: The package requests broader agent tools than its local classification workflow needs.

Mitigation: Allow only the minimum access needed to run the local Python CLI; withhold Write and WebFetch unless separately justified.

Risk: Package integrity metadata is inconsistent.

Mitigation: Review the package before installation and request corrected, verified integrity hashes from the publisher.

Risk: Preliminary classification or registration guidance could be mistaken for an authoritative regulatory decision.

Mitigation: Verify every result against current official regulatory sources or qualified counsel before making filing decisions.

## Reference(s):

- [md-classification-route on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/md-classification-route)

## Skill Output:

**Output Type(s):** [Guidance, JSON]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes provisional class and route hints, warnings, error codes, and status rc=0 (no warnings), 1 (warnings), or 2 (invalid or insufficient input); rc is not a device class.]

## Skill Version(s):

1.0.1 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
