## Description:

Track coffee and caffeine: typical caffeine per drink, today's total against a 400 mg (or 200 mg in pregnancy) limit, how much is still in your system, when it drops low enough for sleep, and reusable vs disposable cups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nbkdevs](https://clawhub.ai/user/nbkdevs)

### License/Terms of Use:

MIT

## Use Case:

People tracking coffee and caffeine can log drinks, review their daily intake and estimated remaining caffeine, estimate when levels fall below a sleep threshold, and count reusable versus disposable cups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The commands run an externally downloaded package without pinning its version, and this review does not verify that implementation.

Mitigation: Review and pin the package version before execution; restrict it to the intended log where practical.

Risk: Drink history persists in ~/.gopromotional-mugday.json and may contain personal usage details.

Mitigation: Protect the local log and use --file or GOPROMOTIONAL_MUGDAY_FILE to choose a controlled storage location.

Risk: Caffeine amounts and sleep-readiness estimates are approximate and may be mistaken for medical advice.

Mitigation: Treat the estimates as informational only and not as medical advice.

## Reference(s):

- [GoPromotional travel mugs](https://www.gopromotional.co.uk/branded-products/travel-mugs)
- [ClawHub skill page](https://clawhub.ai/nbkdevs/skills/gopromotional-mugday)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Human-readable CLI output or JSON with --json]

**Output Parameters:** [Drink name, caffeine amount, timestamp, reusable-cup flag, and sleep threshold]

**Other Properties Related to Output:** [Drink history is saved locally; caffeine and sleep estimates use typical values and a five-hour half-life.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
