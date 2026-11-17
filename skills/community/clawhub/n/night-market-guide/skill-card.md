## Description:

Finds night markets, food streets, street food hotspots, and related travel options using FlyAI and Fliggy results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to look up night markets, food streets, and local culinary points of interest with booking-linked results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on installing and running an unpinned global npm CLI.

Mitigation: Install a pinned, reviewed CLI version manually in an isolated environment before use.

Risk: Travel search parameters may be sent to FlyAI or Fliggy services.

Mitigation: Avoid entering sensitive personal data and review whether sharing destination and travel intent data is acceptable.

Risk: Booking links are commercial results rather than neutral recommendations.

Mitigation: Treat linked results as commercial booking options and compare against independent sources before purchase.

## Reference(s):

- [Night Market Guide on ClawHub](https://clawhub.ai/xiejinsong/skills/night-market-guide)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown travel recommendations with comparison tables and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are expected to include Book links and avoid raw JSON in end-user output.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
