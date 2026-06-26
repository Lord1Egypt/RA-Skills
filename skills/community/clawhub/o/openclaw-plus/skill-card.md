## Description: <br>
Multi-capability dev skill for chained workflows involving Python execution, package management, git, HTTP requests, file operations, process management, sub-agents, or webhook notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shindo957-official](https://clawhub.ai/user/shindo957-official) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation engineers use OpenClaw+ to compose multi-step development workflows such as running Python, installing packages, managing git changes, making HTTP/API requests, editing files, managing processes, delegating sub-tasks, and sending webhook notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad development-agent authority, including code execution, package installation, file operations, commits, process management, sub-agent delegation, and webhooks. <br>
Mitigation: Use it in a disposable or tightly controlled workspace, review generated commands and diffs before commit, and require explicit confirmation before high-impact actions. <br>
Risk: The skill may handle sensitive credentials for authenticated API calls or webhook notifications. <br>
Mitigation: Store credentials in environment variables, avoid sending secrets or private data to unapproved URLs, and validate authenticated endpoints before use. <br>
Risk: Package installation and process execution can alter the runtime environment or leave long-running processes active. <br>
Mitigation: Avoid global or system package installs unless approved, prefer isolated environments, set timeouts, and stop background processes when workflows finish. <br>


## Reference(s): <br>
- [OpenClaw+ ClawHub Page](https://clawhub.ai/shindo957-official/openclaw-plus) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>
- [REFERENCE.md](REFERENCE.md) <br>
- [QUICKSTART.md](QUICKSTART.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file changes, API request plans, process-management steps, git commands, and webhook notification guidance depending on the workflow.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
