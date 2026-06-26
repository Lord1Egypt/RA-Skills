## Description: <br>
Versioned, structured memory for AI agents that tracks facts, logs changes, and helps agents retrieve current context; requires MEMSTATE_API_KEY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yepthatsjason](https://clawhub.ai/user/yepthatsjason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to store, recall, search, version, and clean up structured project memory in Memstate. It supports persistent task context, fact tracking, semantic lookup, history review, and soft deletion through bundled Python scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored content is sent to an external persistent memory service. <br>
Mitigation: Do not store secrets, credentials, regulated data, or confidential project details unless the organization approves that data leaving the local environment. <br>
Risk: MEMSTATE_API_KEY grants access to Memstate operations. <br>
Mitigation: Protect the API key as a secret and avoid exposing it in logs, prompts, repository files, or shared terminal output. <br>
Risk: Recursive and project-level delete commands can remove large sets of active memories. <br>
Mitigation: Confirm the target project and keypath before running recursive or project-level delete commands. <br>


## Reference(s): <br>
- [Memstate AI Homepage](https://memstate.ai) <br>
- [Memstate AI Documentation](https://memstate.ai/docs) <br>
- [Memstate MCP Plugin](https://github.com/memstate-ai/memstate-mcp) <br>
- [Memstate Benchmark](https://github.com/memstate-ai/memstate-benchmark) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON responses from Memstate scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and MEMSTATE_API_KEY; scripts can read, write, search, view history, and soft-delete Memstate memories or projects.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
