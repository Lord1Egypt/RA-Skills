## Description:

Finds OpenTable restaurant options and creates reservation deep links for user-confirmed booking handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikehe123](https://clawhub.ai/user/mikehe123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to search OpenTable availability by location, cuisine, date, time, and party size, or to build a direct booking link for a named restaurant. The user completes any reservation in OpenTable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill works through an attached Chrome profile and may inspect active browser pages.

Mitigation: Use a dedicated or low-risk browser profile and avoid saved payment methods when running the skill.

Risk: The release has under-scoped navigation and persistent browser configuration recovery concerns.

Mitigation: Review before installing and only approve SSRF allowlist changes or profile resets when the operational impact is understood.

Risk: Booking deep links may point to stale, unavailable, or incorrect reservation details because direct booking link construction does not verify live availability.

Mitigation: Have the user review restaurant, time, party size, and payment terms in OpenTable before confirming.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikehe123/skills/opentable-reservations)
- [OpenTable](https://www.opentable.com/)
- [README.md](artifact/README.md)
- [BENCHMARK.md](artifact/BENCHMARK.md)
- [SKILL.md](artifact/SKILL.md)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payloads and OpenTable URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces restaurant summaries and booking deep links; does not submit reservations.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
