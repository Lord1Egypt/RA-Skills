## Description: <br>
Deploy and manage apps, servers, databases, domains, and environment variables on VPS providers using the Hoist CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[g4f4r0](https://clawhub.ai/user/g4f4r0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use Hoist to guide agent-assisted deployment and administration of applications, VPS servers, databases, domains, environment variables, Dockerfiles, and troubleshooting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill helps administer real infrastructure, including creating, modifying, and destroying servers, databases, domains, keys, and environment variables. <br>
Mitigation: Use least-privilege provider tokens and require explicit user confirmation before actions that create, modify, expose, or destroy resources. <br>
Risk: Environment-variable, database, and log outputs may contain secrets or sensitive connection information. <br>
Mitigation: Avoid asking the agent to print or summarize env exports, database connection strings, provider tokens, or logs that may contain secrets. <br>
Risk: Public database exposure and domain changes can unintentionally broaden network access. <br>
Mitigation: Keep services private by default and confirm DNS, firewall, and public-access changes before executing related Hoist commands. <br>


## Reference(s): <br>
- [Hoist homepage](https://github.com/g4f4r0/hoist) <br>
- [Hoist ClawHub listing](https://clawhub.ai/g4f4r0/hoist) <br>
- [COMMANDS.md](COMMANDS.md) <br>
- [DOCKERFILES.md](DOCKERFILES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and Dockerfile snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Hoist CLI commands are expected to return structured JSON in non-TTY agent contexts.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
