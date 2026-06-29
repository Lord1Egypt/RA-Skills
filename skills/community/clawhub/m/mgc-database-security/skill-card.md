## Description: <br>
Secure database credential management using MGC Blackbox for MySQL, PostgreSQL, SQLite, MariaDB, and other databases, with credentials stored locally in encrypted form and retrieved at runtime without exposing them to AI models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zkeviny](https://clawhub.ai/user/zkeviny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this documentation skill to manage database credentials through MGC Blackbox, retrieve them only at runtime, and build database scripts that avoid exposing passwords or connection strings to the agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database credentials could be exposed if users paste secrets into prompts, code, logs, or command output while following the pattern. <br>
Mitigation: Store secrets in MGC Blackbox, retrieve them only at runtime through MCP tools or local scripts, and avoid printing or logging credential values. <br>
Risk: Database operations may affect production data if users apply generated scripts or queries without checking the target connection. <br>
Mitigation: Verify the selected database identifier and environment before execution, use separate credentials per environment, and review query behavior before running against sensitive systems. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JSON, shell command, and conceptual code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation only; no executable code is included in the artifact.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
