## Description:

Price Monitor helps agents track website prices, inventory, and content changes with browser automation, CSV product lists, local history logging, and alert-oriented checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinanping-cpu](https://clawhub.ai/user/yinanping-cpu)

### License/Terms of Use:


## Use Case:

Developers, operators, and analysts use this skill to monitor product prices, inventory status, and website content changes, then capture price history and alert-relevant changes for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Monitoring product or competitor URLs may expose browsing activity and create local price-history records.

Mitigation: Monitor only approved URLs and store generated history files in locations appropriate for the sensitivity of the products or competitors being tracked.

Risk: Email, Discord, cron scheduling, proxies, or user-agent rotation are described as optional additions and can change operational and data-sharing risk.

Mitigation: Review and approve those additions separately before enabling them, especially for business-sensitive monitoring.

Risk: Browser automation can return stale, missing, or incorrect values when selectors change, pages fail to load, or sites block automated access.

Mitigation: Use stable selectors, rerun browser snapshots when extraction fails, and review error rows before acting on alerts.

## Reference(s):

- [Price Monitor on ClawHub](https://clawhub.ai/yinanping-cpu/skills/price-monitor)
- [Publisher profile](https://clawhub.ai/user/yinanping-cpu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples, CSV product configuration, console status output, and local CSV price-history logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When the included monitor script is run, it appends timestamped price check results to a local price-history.csv file and prints significant change alerts to the console.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
