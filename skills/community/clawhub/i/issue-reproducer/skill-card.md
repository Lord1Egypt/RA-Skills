## Description:

Organizes bug descriptions into reproducible steps, environment details, expected and actual results, and minimum reproduction criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and support teams use this skill to turn raw bug reports into structured, reviewable reproduction drafts and checklists while calling out missing information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled Python helper can inspect local files when directory, CSV, pattern, or skill-audit modes are enabled.

Mitigation: Keep resources/spec.json in structured_brief mode for normal use, run it only on narrow non-sensitive inputs, and review the script before enabling audit modes.

Risk: Bug reports and logs may contain sensitive environment details or personal information.

Mitigation: Redact sensitive material before using the skill or writing generated output files.

Risk: A formatted reproduction draft can be misleading if source details are incomplete.

Mitigation: Review the generated draft before filing or sharing it, and preserve explicit missing-information sections instead of filling gaps with assumptions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/issue-reproducer)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Output Specification](artifact/resources/spec.json)
- [Output Template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Structured Markdown, with optional JSON output from the local helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write an output file when the helper script is run with --output; otherwise returns reviewable text.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
