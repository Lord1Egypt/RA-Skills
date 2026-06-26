## Description: <br>
Monitors Polymarket positions, tracks portfolio P&L, emits alerts for resolved positions or large price moves, and can trigger reinvestment workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[themsquared](https://clawhub.ai/user/themsquared) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor a Polymarket wallet, summarize open and resolved positions, and send alert output that can support portfolio oversight. It is also designed to run on a schedule and coordinate with separate reinvestment, weather scanning, and exit-management scripts when those are supplied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitor can operate with wallet credentials and includes a hardcoded wallet fallback. <br>
Mitigation: Use a dedicated low-balance wallet, replace the hardcoded wallet value, and keep private keys in protected environment variables outside logs and shell history. <br>
Risk: Scheduled or daemon execution can repeatedly invoke trading-related helper scripts. <br>
Mitigation: Do not enable cron or daemon mode until explicit trading limits, dry-run behavior, and a clear stop mechanism are in place. <br>
Risk: The artifact references helper scripts that are not included in the release. <br>
Mitigation: Inspect or supply the missing helper scripts before enabling reinvestment, weather scanning, or exit-management behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/themsquared/polymarket-portfolio-tracker-v2) <br>
- [Publisher profile](https://clawhub.ai/user/themsquared) <br>
- [Polymarket Data API endpoint](https://data-api.polymarket.com) <br>
- [Polymarket Gamma API endpoint](https://gamma-api.polymarket.com) <br>
- [Polymarket CLOB API endpoint](https://clob.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with shell and Python snippets; runtime output is plain text alert content and JSON state files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local state files for position snapshots and daily P&L when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, released 2026-03-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
