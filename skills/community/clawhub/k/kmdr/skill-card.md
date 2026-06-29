## Description: <br>
Guides an agent in using the kmdr CLI to search Kmoe manga, plan downloads, start background downloads, check quota and progress, and manage credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrisis58](https://clawhub.ai/user/chrisis58) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate the Kmoe Manga Downloader CLI for manga search, download planning, quota checks, background download tracking, and credential-pool management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and invokes an external kmdr CLI package and uses the Kmoe service. <br>
Mitigation: Confirm trust in the external CLI package and Kmoe service before installation or execution. <br>
Risk: Login commands can expose passwords if credentials are passed through the agent chat. <br>
Mitigation: Prefer user-managed terminal login so passwords do not enter the conversation history. <br>
Risk: Background downloads and saved credentials or configuration may persist outside the current conversation. <br>
Mitigation: Review the configured download destination and credential/configuration state before starting downloads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrisis58/skills/kmdr) <br>
- [Kmoe website](https://kxx.moe/) <br>
- [JSON output format](references/output-format.md) <br>
- [Error status codes](references/error-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and NDJSON output interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external kmdr CLI, valid credentials, and review of structured result codes before recovery actions.] <br>

## Skill Version(s): <br>
1.0.0-a3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
