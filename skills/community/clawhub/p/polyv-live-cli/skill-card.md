## Description: <br>
Helps authorized PolyV operators use the published polyv-live-cli npm package to query and manage PolyV live-streaming channels, playback, products, viewers, interactions, access controls, platform settings, and statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polyv](https://clawhub.ai/user/polyv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support engineers, and live operations teams use this skill to choose and validate PolyV CLI commands for administering live-streaming channels, viewer access, interactive features, commerce, playback, and reporting. It is intended for authorized PolyV account operators who can verify account context before making changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mutating commands can change live PolyV channels, viewer-facing features, account settings, or production state. <br>
Mitigation: Require explicit authorization for write, delete, start, stop, push, import, merge, transcode, and similar operations; verify the active account and resource IDs before execution. <br>
Risk: CLI output can include sensitive operational data such as viewer records, donation records, chat logs, check-in results, passwords, stream credentials, or AppSecret values. <br>
Mitigation: Treat exported data and credentials as sensitive, avoid echoing AppSecret values, and share stream credentials only with trusted streaming endpoints when explicitly requested. <br>
Risk: Reference examples or cached command shapes may differ from the currently published npm CLI. <br>
Mitigation: Validate command syntax with the relevant polyv-live-cli --help output before use and prefer JSON output for downstream processing. <br>


## Reference(s): <br>
- [PolyV official website](https://www.polyv.net/) <br>
- [PolyV live API documentation](https://help.polyv.net/#/live/api/) <br>
- [Task routing reference](references/task-routing.md) <br>
- [Command index](references/command-index.md) <br>
- [Authentication reference](references/authentication.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON-oriented command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands rely on the current npm latest polyv-live-cli help output and may require configured PolyV credentials.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
