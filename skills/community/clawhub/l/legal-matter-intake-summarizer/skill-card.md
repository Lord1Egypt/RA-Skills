## Description:

Organizes legal intake materials into facts, dispute points, known evidence, missing materials, follow-up questions, and risk notes without providing legal conclusions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Legal operations teams, intake staff, and agents use this skill to turn supplied matter materials into a reviewable structured brief and checklist before attorney review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the structured intake draft for legal advice or attorney review.

Mitigation: Present the output as an organizational draft, preserve the skill's no-legal-conclusions boundary, and route the matter to qualified legal review before relying on it.

Risk: Legal intake materials may contain sensitive personal or case information.

Mitigation: Use only an appropriate local workspace and output path, and redact or avoid unnecessary sensitive materials before processing.

Risk: The helper script can write generated output to a local file path selected by the user.

Mitigation: Review the target path before execution and use dry-run or stdout output when file writes are not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/legal-matter-intake-summarizer)
- [ClawHub publisher profile](https://clawhub.ai/user/52yuanchangxing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured Markdown, with optional JSON from the local helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python 3 and standard-library code only; supports local file input, local file output, dry-run mode, and markdown/json format selection.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
