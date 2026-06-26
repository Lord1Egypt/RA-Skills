## Description: <br>
Controls a local multi-account browser management tool to list, start, stop, and query browser accounts through its HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wociaozhongyunonghaole](https://clawhub.ai/user/wociaozhongyunonghaole) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who already use the local multi-account matrix management tool can use this skill to run account list, start, and stop workflows from an agent while preserving readable UTF-8 results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start or stop browser accounts in the connected local multi-account tool. <br>
Mitigation: Install and use it only when you intentionally want an agent to control those accounts, and review the requested account name or index before execution. <br>
Risk: Fuzzy name matching may select an unintended account when account names are similar. <br>
Mitigation: Use exact account names or explicit indexes when possible, and resolve multiple-match prompts before starting or stopping an account. <br>
Risk: Operation results are saved locally in last_result.txt. <br>
Mitigation: Treat the result file as local operational output and remove it when account names or status details should not remain on disk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wociaozhongyunonghaole/multi-account-launcher) <br>
- [Publisher profile](https://clawhub.ai/user/wociaozhongyunonghaole) <br>
- [Multi-account matrix management tool](https://zmt.scys6688.com/) <br>
- [Python downloads](https://www.python.org/downloads/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text status results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes UTF-8 operation results to last_result.txt in the skill directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
