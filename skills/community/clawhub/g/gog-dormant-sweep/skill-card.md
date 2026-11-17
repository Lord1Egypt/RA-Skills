## Description:

Scans a GOG library for installed games not played in 30 or more days, emails a summary report through himalaya, and can add per-game cleanup reminders to Apple Reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to review installed GOG games that appear dormant, preview cleanup candidates, and optionally automate email and Apple Reminders follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can send email through the configured himalaya account.

Mitigation: Use --dry-run first, verify the recipient address, or run with --no-email when only analysis is intended.

Risk: The workflow can create Apple Reminders entries for each dormant game.

Mitigation: Confirm Apple Reminders access and the target list, or run with --no-reminders when reminder creation is not intended.

Risk: Dormancy decisions depend on the supplied GOG library JSON fields.

Mitigation: Review the dry-run report before allowing email or reminder side effects.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/gog-dormant-sweep)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain-text report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger email and reminder side effects unless dry-run or skip flags are used.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
