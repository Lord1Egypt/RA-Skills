## Description: <br>
Manage and interact with a user's Matter reading library through the Matter CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicholope](https://clawhub.ai/user/nicholope) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers with a Matter Pro account use this skill to browse, search, summarize, tag, archive, save, and review content in a Matter reading library. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read saved-reading library content, highlights, and account information. <br>
Mitigation: Use narrow requests for library, inbox, highlight, and article access, and avoid broad retrieval unless the user explicitly asks for it. <br>
Risk: The skill can change the user's Matter library by saving, tagging, archiving, updating, or deleting items. <br>
Mitigation: Confirm user intent before write operations such as archive, tag, save, update, or delete. <br>
Risk: Large bulk reads with --all can hit rate limits mid-stream and produce incomplete or corrupted JSON. <br>
Mitigation: Use cursor pagination with documented delays, and stop and wait when a rate-limit error provides a retry interval. <br>


## Reference(s): <br>
- [Matter CLI command reference](references/commands.md) <br>
- [Matter CLI GitHub repository](https://github.com/getmatterapp/matter-cli) <br>
- [Matter CLI ClawHub release](https://clawhub.ai/nicholope/matter-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Matter CLI shell commands and JSON-producing CLI usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Matter CLI commands return JSON by default and can use --plain for human-readable output.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
