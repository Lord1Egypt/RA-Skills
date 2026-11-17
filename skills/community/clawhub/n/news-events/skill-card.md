## Description:

Monitors 20+ premium RSS feeds for breaking news, matches stories to Polymarket markets by keyword analysis, and trades when estimated price impact exceeds 12%.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mibayy](https://clawhub.ai/user/mibayy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run an automated news-monitoring trader that filters recent RSS stories, matches them to active Polymarket markets, and produces dry-run or live trading actions when estimated impact crosses its threshold.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute live automated trading when explicitly run with --live.

Mitigation: Review and constrain live trading before installation, run dry-run first, and require a second confirmation before enabling live mode.

Risk: Trading credentials and account funds may be exposed to unnecessary scope.

Mitigation: Scope SIMMER_API_KEY to minimal funds and permissions and store credentials outside shared project files.

Risk: Plaintext HTTP feeds and temporary shared state can weaken integrity and privacy.

Mitigation: Remove or replace plaintext HTTP feeds where possible and store state in a private per-user directory.

Risk: Dependency behavior may change between installs.

Mitigation: Pin dependencies and review the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mibayy/skills/news-events)
- [Publisher profile](https://clawhub.ai/user/mibayy)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration]

**Output Format:** [Console logs and API trade requests, with command-line execution modes for dry-run, live trading, and quiet cron operation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; dry-run is the default and live trading requires the --live flag.]

## Skill Version(s):

2.0.3 (source: release evidence, SKILL.md frontmatter, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
