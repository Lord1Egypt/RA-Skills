## Description:

Hire a private car with driver for customized day tours, with related travel booking support powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travel users and travel-support agents use this skill to search private-car day tour, half-day, and multi-day driver options, then present bookable results in Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing and running an unpinned global FlyAI CLI.

Mitigation: Install only after user approval, prefer a pinned local installation, and verify the CLI version before use.

Risk: The skill limits travel results to a specific provider and requires booking links and branding.

Mitigation: Tell users results are provider-limited and verify booking details on the linked provider page before purchase.

Risk: The artifact instructs agents not to answer travel availability or pricing from memory.

Mitigation: Use only current FlyAI CLI output for prices, availability, and booking details, and fail closed when the CLI is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/poll-test-1775879470)
- [Publisher profile](https://clawhub.ai/user/xiejinsong)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires results to come from FlyAI CLI output and include provider booking links when presenting travel options.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
