## Description: <br>
Manage Keyco assets, DUBs (QR/NFC/BLE/Virtual beacons), workflows, lifecycle events, users, and analytics through the Keyco CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[husamabdel](https://clawhub.ai/user/husamabdel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, administrators, and developers use this skill to inspect Keyco asset inventory, run analytics, manage lifecycle events, handle assignments, and work with API keys through the Keyco CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide production-changing Keyco administration and credential-management actions. <br>
Mitigation: Require clear user confirmation before delete, revoke, clear, create, assign, or other production-changing commands. <br>
Risk: The setup script may install @keyco/cli globally and can retry with sudo if the first install fails. <br>
Mitigation: Have the user review and explicitly approve setup, and prefer least-privilege installation where possible. <br>
Risk: Keyco API keys grant access to asset and administrative operations. <br>
Mitigation: Use least-privilege API key scopes and avoid exposing keys in prompts, logs, or shared files. <br>
Risk: Manual location updates or workflow completion could bypass Keyco audit integrity. <br>
Mitigation: Use verified scan, heartbeat, lifecycle event, or dashboard override flows instead of attempting direct out-of-band updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/husamabdel/keyco) <br>
- [Keyco CLI command reference](references/cli-commands.md) <br>
- [Keyco API scopes](references/scopes.md) <br>
- [Keyco data integrity guidelines](references/data-integrity.md) <br>
- [Keyco docs](https://docs.qrdub.com) <br>
- [Keyco dashboard](https://dashboard.qrdub.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and summarized command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JSON CLI output when parsing or transforming Keyco data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
