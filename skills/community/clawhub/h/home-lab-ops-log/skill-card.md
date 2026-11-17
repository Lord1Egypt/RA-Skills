## Description:

Home Lab Ops Log helps users turn homelab or personal server change notes into structured, reviewable Markdown ops logs with rollback plans, observations, and follow-up tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Homelab operators and self-hosting developers use this skill to convert change notes, machine context, observed results, and risks into reviewable Markdown operations logs with rollback plans and follow-up tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Homelab change notes can contain sensitive host inventories, credentials, or private infrastructure details.

Mitigation: Redact secrets and sensitive host details before giving content to the skill or its local script.

Risk: Changing the bundled spec from the default structured logging mode to audit modes can cause the script to inspect local files or directories.

Mitigation: Keep the released default mode unless local inspection is intentional, and pass only the intended input paths.

Risk: Sparse input can produce an incomplete operations record.

Mitigation: Review the generated draft and resolve pending confirmation items before treating it as an operational log.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/home-lab-ops-log)

## Skill Output:

**Output Type(s):** [markdown, guidance, shell commands]

**Output Format:** [Markdown or JSON report; Markdown is the default.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write an output file when the local script is invoked with --output; otherwise prints to stdout.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
