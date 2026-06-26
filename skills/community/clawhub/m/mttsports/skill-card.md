## Description: <br>
Use when the user wants to play or observe MTT poker through the `mttsports` CLI: auth, user balance, room selection and creation, table join or add-on, session daemon lifecycle, NDJSON event watching, and in-game actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songlairui](https://clawhub.ai/user/songlairui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to operate MTT Sports poker workflows through the local CLI, including authentication, balance checks, room selection, table joining, session watching, and gameplay actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend account balance and run autonomous MTT Sports poker gameplay. <br>
Mitigation: Before autonomous play, set explicit limits for stakes, buy-in, total loss, add-ons, insurance, all-in actions, and session duration. <br>
Risk: Autonomous table actions may execute without per-hand confirmation once a watch loop is active. <br>
Mitigation: Use a strategy file or session setup step to define risk boundaries before play, and stop the watcher and daemon when automation should end. <br>
Risk: A watcher or daemon launch may fail while the operator assumes automation is active. <br>
Mitigation: Confirm watcher readiness through task status, PID checks, or startup logs, and report immediately when the watch loop is not running. <br>
Risk: Authentication state and tokens are required to operate the account. <br>
Mitigation: Check login status before room or session commands, avoid exposing raw passwords or tokens, and do not write extra copies of sensitive credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/songlairui/mttsports) <br>
- [Publisher Profile](https://clawhub.ai/user/songlairui) <br>
- [MTT Sports CLI npm package](https://www.npmjs.com/package/@mtt-open/mttsports-cli) <br>
- [Session lifecycle reference](artifact/session/references/lifecycle.md) <br>
- [Session operate reference](artifact/session/references/operate.md) <br>
- [Session watch reference](artifact/session/references/watch.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON command-output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses structured CLI commands and NDJSON watch events for session automation.] <br>

## Skill Version(s): <br>
0.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
