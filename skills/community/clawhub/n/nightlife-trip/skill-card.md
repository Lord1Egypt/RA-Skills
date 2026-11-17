## Description:

Book flights for nightlife trips featuring night markets and entertainment districts, using live flyai CLI results and booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to collect route and date details, run live flyai flight searches, and return concise Markdown results with booking links for nightlife-focused trips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may download and globally install an unpinned third-party npm CLI.

Mitigation: Review the package before installation and use only environments where global npm installation is allowed.

Risk: The skill executes user-derived shell command templates for live travel searches.

Mitigation: Validate route, date, and supported flags before execution, and use only documented parameters.

Risk: The skill presents live travel prices and provider booking links.

Mitigation: Confirm booking details and provider terms before purchase, and do not fabricate results when CLI data is unavailable.

## Reference(s):

- [Parameter Collection and Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/skills/nightlife-trip)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live flyai CLI results for flight options; returned flight results must include booking links.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
