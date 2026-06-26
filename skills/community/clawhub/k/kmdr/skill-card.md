## Description: <br>
kmdr helps agents search Kmoe, download manga volumes, track background download progress, and manage local Kmoe credentials and quota. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrisis58](https://clawhub.ai/user/chrisis58) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate the kmdr CLI for Kmoe manga search, download planning, background downloads, progress checks, and credential pool management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses local Kmoe credentials and may expose usernames, passwords, cookies, or quota information if credentials are shared with an agent or shown in outputs. <br>
Mitigation: Prefer manual login, avoid sharing passwords in chat, review any displayed credential data, and remove stored credentials on shared or sensitive machines. <br>
Risk: The kmdr configuration supports a post-download callback command, which can run local commands after downloads. <br>
Mitigation: Use callback configuration only when the exact command is trusted and understood. <br>
Risk: Downloads can consume account quota and write files to local destinations. <br>
Mitigation: Run download planning with --explain before large downloads and use explicit destination paths. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chrisis58/kmdr) <br>
- [Kmoe website](https://kxx.moe/) <br>
- [Command Reference](references/commands.md) <br>
- [JSON Output Format](references/output-format.md) <br>
- [Error Codes](references/error-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON result interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are expected to use kmdr toolcall mode and return structured result or progress JSON.] <br>

## Skill Version(s): <br>
1.0.0-a1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
