## Description: <br>
OpenCode CLI integration skill that helps agents run coding tasks through OpenCode CLI with a plan-to-build workflow, session management, MCP integration, and background task monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tchen6500](https://clawhub.ai/user/tchen6500) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to plan, run, monitor, and continue OpenCode CLI coding sessions in trusted repositories. It is most useful for multi-step implementation work, MCP-assisted UI or database tasks, and background coding workflows that need active progress checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to run OpenCode CLI with coding and shell capabilities in a repository. <br>
Mitigation: Use it only in trusted repositories and review proposed commands, code changes, and test results before accepting them. <br>
Risk: Optional MCP servers may run local tools or third-party packages, including UI automation, context, or database integrations. <br>
Mitigation: Review each MCP server before use, prefer verified global installs, and avoid dynamic package execution when possible. <br>
Risk: Supabase or Context7 credentials may be provided to configured MCP servers. <br>
Mitigation: Provide credentials only when needed, scope them narrowly, and keep secrets out of prompts, logs, and version control. <br>
Risk: Database prompts, SQL, and migrations can alter project data. <br>
Mitigation: Verify database operations carefully, use least-privilege credentials, and back up important data before applying migrations. <br>


## Reference(s): <br>
- [Built-in Tools Guide](references/built-in-tools-guide.md) <br>
- [MCP Configuration Guide](references/mcp-config-guide.md) <br>
- [Skills Configuration Guide](references/skills-config-guide.md) <br>
- [Practical Tips Guide](references/tips-guide.md) <br>
- [OpenCode Documentation](https://opencode.ai/docs) <br>
- [AgentSkills Specification](https://agentskills.io/specification) <br>
- [ClawHub Skill Page](https://clawhub.ai/tchen6500/opencode-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that invoke OpenCode CLI and optional MCP servers; review commands and configuration before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
