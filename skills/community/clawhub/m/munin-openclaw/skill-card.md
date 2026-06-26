## Description: <br>
Munin - The Free (or $1.6/mo) Persistent Memory for OpenClaw. Stop your agent from having Alzheimer's. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[3d-era](https://clawhub.ai/user/3d-era) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this adapter to give agents persistent Munin-backed memory through CLI actions or an MCP server. It supports capabilities checks and project-scoped memory actions against a configured Munin endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory operations are sent to the configured Munin endpoint and may include sensitive user or agent context. <br>
Mitigation: Use only a trusted MUNIN_BASE_URL and avoid storing credentials, regulated data, or other highly sensitive content unless that storage risk has been separately accepted. <br>
Risk: The Munin API key authorizes access to memory operations and could be exposed through prompts, logs, or source control. <br>
Mitigation: Treat MUNIN_API_KEY as a secret, keep it out of prompts and repositories, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/3d-era/munin-openclaw) <br>
- [Publisher profile](https://clawhub.ai/user/3d-era) <br>
- [Munin cloud endpoint](https://munin.kalera.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MUNIN_BASE_URL and optionally MUNIN_API_KEY for authenticated Munin access.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
