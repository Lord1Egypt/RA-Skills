## Description: <br>
Guides agents to use the otta CLI for otta.fi worktime, absence, sick-leave, status, calendar, and reporting workflows with JSON-first terminal commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mekedron](https://clawhub.ai/user/mekedron) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and employees use this skill to guide agents through Otta time-tracking workflows such as authentication, worktime changes, absence lookup, holiday retrieval, saldo checks, and calendar reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can update or delete Otta worktime records. <br>
Mitigation: Show the target worktime record and obtain explicit user confirmation before update or delete operations. <br>
Risk: Credentials or tokens could be exposed through command arguments, logs, or summaries. <br>
Mitigation: Prefer password-stdin or secret environment handling, and never print raw credentials or tokens in summaries. <br>
Risk: Incorrect API base URL, config path, or cache path could direct operations to the wrong account or environment. <br>
Mitigation: Verify the API base URL and config/cache paths before account-changing operations, and run status with JSON output when cached identity is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mekedron/otta-cli) <br>
- [Otta CLI repository listed by the skill](https://github.com/mekedron/otta-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers --format json for data-producing commands and requires credentials or tokens to be omitted from summaries.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
