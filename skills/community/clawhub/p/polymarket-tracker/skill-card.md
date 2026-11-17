## Description:

Tracks top active Polymarket markets by trading volume, showing market names, approximate Yes/No volume splits, current odds, and requiring 0.001 USDT skillpay.me payment per normal call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ariesdevil](https://clawhub.ai/user/ariesdevil)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to identify high-volume active Polymarket markets and review current Yes/No odds before further analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reported volumes can be mistaken for recent trading momentum because the authoritative security guidance identifies them as lifetime aggregate values.

Mitigation: Present reported volume as lifetime aggregate and treat Yes/No splits as approximate before using the output for market analysis.

Risk: Normal use charges 0.001 USDT through skillpay.me.

Mitigation: Confirm the user ID, balance, and payment expectation before running a paid call; use balance-check or test mode when appropriate.

Risk: Passing the billing API key directly on the command line can expose it in local process lists or shell history.

Mitigation: Prefer environment variables or another secret-handling mechanism and avoid sharing logs that contain credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ariesdevil/skills/polymarket-tracker)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [skillpay.me billing service](https://skillpay.me)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text market ranking with command-line billing and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the top 10 active markets; volume is lifetime aggregate, Yes/No volume splits are approximate, and normal use charges 0.001 USDT.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
