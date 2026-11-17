## Description:

Checks submission-document folders for missing, expired, or inconsistent records and cites the files and pages behind its findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Applicants and their agents use this skill to check visa, rental, insurance, and other submission packets against a selected checklist before filing. It produces cited findings and an inventory, not an eligibility determination or legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit recursively reads a chosen folder of potentially sensitive application documents and writes extracted details into local reports.

Mitigation: Choose the input folder deliberately and keep the report output in a private location.

Risk: PDF extraction may vary with the available runtime.

Mitigation: Use a pinned runtime when reproducible PDF results matter.

## Reference(s):

- [Packet Audit on ClawHub](https://clawhub.ai/deepseekoracle/skills/packet-audit)
- [Finding codes](references/finding-codes.md)
- [Authoring a profile](references/authoring-a-profile.md)
- [Limitations](references/limits.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Text summary with Markdown and JSON report files and a JSON packet manifest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source files and PDF pages; the manifest records per-file SHA-256 hashes.]

## Skill Version(s):

1.1.1 (source: SKILL.md metadata, CHANGELOG, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
