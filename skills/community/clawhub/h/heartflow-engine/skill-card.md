## Description: <br>
HeartFlow is a local JavaScript cognitive substrate for agents that produces structured cognitive state across memory, emotion, reasoning, decision routing, search, and optional code execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yun520-1](https://clawhub.ai/user/yun520-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add a local cognitive analysis layer that returns structured state for intent, emotion, memory, judgment, decision routing, and related agent workflows. It can also be integrated through a CLI, Node.js API, or local MCP server when explicit deployment controls are in place. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-impact local behavior, including optional code execution and file-writing, can affect the host environment if enabled for untrusted inputs. <br>
Mitigation: Keep code execution disabled unless inputs are trusted, review proposed commands and file-write routes before integration, and run the skill with least-privilege filesystem access. <br>
Risk: Persistent memory can retain sensitive conversation or project data in the local memory directory. <br>
Mitigation: Avoid storing sensitive conversations, configure an appropriate data directory, and review retention or deletion practices before deployment. <br>
Risk: A local MCP server can expose agent tools if bound or configured too broadly. <br>
Mitigation: Set an MCP token, keep the server scoped to trusted clients, and avoid exposing the endpoint beyond the intended local or controlled environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yun520-1/skills/heartflow-engine) <br>
- [README](README.md) <br>
- [Installation guide](INSTALL.md) <br>
- [HeartFlow v5.4.1 upgrade report](docs/upgrade-v5.4.1.md) <br>
- [Security audit report v5.3.0](docs/audit-report-v5.3.0.md) <br>
- [Benchmark report](docs/benchmark-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured text with code, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce structured cognitive state for downstream agents; optional code execution, file writes, network access, and MCP serving require explicit configuration or opt-in.] <br>

## Skill Version(s): <br>
5.4.1 (source: server release, SKILL.md frontmatter, package.json, VERSION.txt) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
