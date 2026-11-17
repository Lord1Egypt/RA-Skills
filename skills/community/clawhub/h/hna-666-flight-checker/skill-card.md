## Description:

Queries Hainan Airlines 666Plus round-trip flight eligibility and automatically checks configured destinations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aywd2026](https://clawhub.ai/user/aywd2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to check whether Hainan Airlines 666Plus benefits have available round-trip routes between Beijing and configured destinations for user-supplied outbound and return dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches Playwright and submits automated searches to Hainan Airlines' mobile query page.

Mitigation: Review the airline site's terms and run the skill only when automated querying for the selected dates and destinations is acceptable.

Risk: The documented execution command includes a hardcoded local path and Playwright environment.

Mitigation: Adjust paths and verify the Playwright runtime before deployment.

Risk: The skill is primarily documented in Chinese, which may affect operator understanding.

Mitigation: Have a Chinese-capable reviewer confirm intended behavior, inputs, and output interpretation before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aywd2026/skills/hna-666-flight-checker)
- [Hainan Airlines 666Plus query page](https://m.hnair.com/hnams/plusMember/ableAirlineQuery)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires outbound and return dates; output lists eligible round-trip destinations when found.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
