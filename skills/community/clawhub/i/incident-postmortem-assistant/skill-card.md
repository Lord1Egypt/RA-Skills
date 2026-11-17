## Description:

Organizes incident evidence into a reviewable postmortem draft that separates root causes, contributing factors, amplifiers, impact, remediation actions, and follow-up improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

SRE, operations, and engineering teams use this skill to turn incident timelines, alerts, handling notes, and impact details into structured, reviewable postmortem drafts and improvement checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incident notes may contain private operational details or personal data.

Mitigation: Review and redact sensitive input before using the skill or sharing generated drafts.

Risk: Broad directory inputs can produce noisy or unintended summaries.

Mitigation: Point the local script at intended incident files or narrow directories only.

Risk: Unused generic audit modes may confuse maintainers or reviewers.

Mitigation: Document or remove dormant modes before relying on the skill in a managed release process.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/incident-postmortem-assistant)
- [Publisher Profile](https://clawhub.ai/user/52yuanchangxing)
- [Artifact README](artifact/README.md)
- [Skill Specification](artifact/resources/spec.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown by default; optional JSON when the local script is run with --format json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local input only and asks for missing incident details instead of filling gaps.]

## Skill Version(s):

1.0.0 (source: server release, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
