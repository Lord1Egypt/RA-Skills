## Description: <br>
Search and answer questions over documents already uploaded to NotebookLM using the nlm CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lhquangit](https://clawhub.ai/user/lhquangit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and operators use this skill to query existing NotebookLM notebooks from an agent workflow, including Telegram-driven questions and source lookups. It is intended for environments where the NotebookLM CLI and authentication storage have already been configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Raw Telegram `/nlm` input can be forwarded to the NotebookLM CLI. <br>
Mitigation: Limit access to trusted users, review commands before enabling broad use, and prefer read-only NotebookLM query workflows. <br>
Risk: The release includes privileged VPS bootstrap scripts. <br>
Mitigation: Review the bootstrap before running it with sudo and install only on controlled systems. <br>
Risk: NotebookLM authentication uses reusable Google session cookies. <br>
Mitigation: Store auth files with restrictive permissions, never commit or share them, and rotate or revoke cookies if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lhquangit/notebooklm-cli-cookies) <br>
- [NotebookLM CLI skill guide](docs/GUIDELINE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command output summaries with inline shell commands when setup or verification is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should identify the queried notebook when available and should report when NotebookLM does not contain an answer.] <br>

## Skill Version(s): <br>
0.1.4 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
