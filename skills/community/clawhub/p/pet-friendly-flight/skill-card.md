## Description:

Search for pet-friendly flights with animal cabin and pet carrier options, plus related travel booking support for hotels, trains, attractions, itinerary planning, visa information, travel insurance, car rental, and more through Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to collect route details, run flyai flight searches, and format pet-friendly flight options with booking links and pet travel guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires global installation and execution of an unpinned third-party flyai CLI for matching searches.

Mitigation: Require explicit approval before installation, prefer a pinned or sandboxed CLI, and verify the installed package before use.

Risk: The skill steers recommendations to mandatory booking links, which can affect purchases.

Mitigation: Independently check airline pet policies, prices, availability, and booking-link destinations before purchase.

Risk: Incorrect or incomplete route parameters could produce misleading search results.

Mitigation: Validate origin, destination, date, and sort options with the user before running booking-related commands.

## Reference(s):

- [Skill source](artifact/SKILL.md)
- [Parameter Collection and Output Templates](artifact/references/templates.md)
- [Scenario Playbooks](artifact/references/playbooks.md)
- [Failure Recovery](artifact/references/fallbacks.md)
- [Execution Runbook](artifact/references/runbook.md)
- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/pet-friendly-flight)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links, comparison tables, pet travel tips, and inline shell commands when execution is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CLI-derived travel results and should not include raw JSON in user-facing responses.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
