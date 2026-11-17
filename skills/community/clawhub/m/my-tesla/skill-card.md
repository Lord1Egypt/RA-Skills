## Description:

Control Tesla vehicles from macOS via the Tesla Owner API using teslapy for authentication, vehicle status, reports, and safety-gated remote commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[officialpm](https://clawhub.ai/user/officialpm)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect Tesla vehicle state, generate chat-friendly or JSON reports, and issue deliberate remote commands for locking, climate, charging, windows, seats, sentry mode, charge-port actions, and mileage logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read Tesla account and vehicle data and issue remote commands to a vehicle.

Mitigation: Install only when this access is intended, review commands before running them, and rely on the documented confirmation flags for disruptive actions.

Risk: Local token cache, default-car settings, logs, and mileage database files can contain sensitive account or vehicle information.

Mitigation: Keep ~/.tesla_cache.json, ~/.my_tesla.json, and ~/.my_tesla/mileage.sqlite out of shared or synced locations and review local file permissions.

Risk: Raw vehicle-data output can include precise location or other sensitive vehicle details.

Mitigation: Prefer sanitized summary or report JSON for routine use, and request raw JSON or precise location only when explicitly needed.

Risk: Hourly mileage logging can create ongoing local records and may wake vehicles under the configured policy.

Mitigation: Enable the launchd example only deliberately and use no-wake or conservative auto-wake settings appropriate for the use case.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/officialpm/skills/my-tesla)
- [Publisher Profile](https://clawhub.ai/user/officialpm)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plus CLI text or JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports sanitized JSON for common reports and raw vehicle data only when explicitly requested.]

## Skill Version(s):

0.1.64 (source: server release metadata, VERSION.txt, changelog released 2026-01-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
