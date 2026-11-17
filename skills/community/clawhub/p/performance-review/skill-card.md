## Description:

Performance Review generates Chinese-language performance review materials, including self-assessments, manager feedback, KPI summaries, promotion narratives, SMART goals, OKR conversions, and 360-degree feedback templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, managers, and HR reviewers use this skill to draft structured performance review text, KPI summaries, promotion narratives, goals, and feedback templates from user-provided role, achievement, target, and feedback details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive employee feedback, KPI data, promotion details, or other personnel information may be entered into the skill.

Mitigation: Review inputs before use, avoid confidential personnel data unless approved, and handle generated review text under the organization's HR data policies.

Risk: The package includes an under-documented utility that can persist user-entered text in a local data directory and may misrepresent removal behavior.

Mitigation: Use the documented review generator for normal workflows, avoid scripts/script.sh for sensitive data, and inspect or disable local persistence before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/performance-review)
- [Performance review tips and best practices](artifact/tips.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text and Markdown-style templates with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated locally from command-line arguments and may contain placeholders for reviewer completion.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
