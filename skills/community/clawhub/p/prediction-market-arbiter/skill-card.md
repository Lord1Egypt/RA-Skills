## Description:

Cross-platform divergence scanner comparing Kalshi and Polymarket prices on identical events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingmadellc](https://clawhub.ai/user/kingmadellc)

### License/Terms of Use:

MIT-0

## Use Case:

External traders, analysts, and developers use this skill to compare Kalshi and Polymarket markets, identify likely matching events, and surface cross-platform price divergences for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Kalshi trading credentials.

Mitigation: Use a dedicated environment and configure a read-only Kalshi API key before running the scanner.

Risk: The documentation includes a complete-stack install command that installs additional skills.

Mitigation: Install only this skill unless each additional stack component has been reviewed.

Risk: The scanner writes local cache files under the user's home directory.

Mitigation: Review local cache contents and retention expectations before scheduled or shared-environment use.

Risk: The scanner makes outbound calls to Kalshi and Polymarket.

Mitigation: Run it only in environments where those network calls are expected and permitted.

## Reference(s):

- [Fuzzy Title Matching Technical Deep Dive](references/fuzzy-matching.md)
- [Kalshi](https://kalshi.com)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [Prediction Market Arbiter on ClawHub](https://clawhub.ai/kingmadellc/skills/prediction-market-arbiter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, YAML configuration examples, console alerts, and JSON cache files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ranked divergence alerts and writes local cache data for follow-up analysis.]

## Skill Version(s):

1.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
