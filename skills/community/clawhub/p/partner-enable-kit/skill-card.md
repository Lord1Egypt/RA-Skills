## Description:

Generates structured partner and channel enablement kits with partner profiles, required materials, FAQs, blockers, version differences, and update rhythms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Channel managers, partner enablement teams, and sales enablement teams use this skill to turn partner type, product scope, and target scenario inputs into reviewable enablement-kit drafts and execution checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input materials may include sensitive internal policies or partner information.

Mitigation: Use only content approved for this drafting workflow and redact sensitive or personal data before processing.

Risk: Generated enablement drafts may contain incomplete or unapproved claims if source input is thin.

Mitigation: Review the draft, resolve listed confirmation items, and verify facts before sharing with partners.

Risk: The optional script can write generated content to a chosen local path.

Mitigation: Choose an output path intentionally, use dry-run or stdout for review when appropriate, and avoid overwriting important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/partner-enable-kit)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)
- [README](artifact/README.md)
- [Skill specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown by default, with optional JSON from the local script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional script can write output to a user-selected path or print to stdout; no third-party Python dependencies are required.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
