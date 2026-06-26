## Description: <br>
Buildable Bring Your Own Context system for AI agents that helps create owned context vaults, scaffold typed memory systems, generate MCP-native context layers, build portable bundle workflows, migrate context across runtimes, and audit long-running agent memory systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielfoojunwei](https://clawhub.ai/user/danielfoojunwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI infrastructure teams use this skill to build, audit, or migrate user-owned or organization-owned context systems for agents, including typed memory workspaces, governance policies, evaluation scorecards, portable bundles, and MCP interfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and mutate a local context workspace that may hold durable user or organization memory. <br>
Mitigation: Generate into a fresh directory, review generated files before connecting the MCP server, and install dependencies in an isolated environment. <br>
Risk: MCP HTTP transport can expose memory operations if bound to an untrusted environment. <br>
Mitigation: Keep HTTP transport local or otherwise trusted, and prefer stdio for local agent integrations unless remote access is explicitly required and secured. <br>
Risk: Permanent deletion of memory objects is irreversible without backups. <br>
Mitigation: Use tombstone deletion first when possible, keep backups for important context stores, and rebuild bundle manifests after deletion. <br>


## Reference(s): <br>
- [Context Architecture Guide](references/context_architecture.md) <br>
- [Evaluation and Governance Guide](references/evaluation_and_governance.md) <br>
- [Paradigm Shifts for Portable Context Systems](references/paradigm_shifts.md) <br>
- [Model Context Protocol Introduction](https://modelcontextprotocol.io/docs/getting-started/intro) <br>
- [Claude Memory Tool Documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) <br>
- [OpenAI Memory FAQ](https://help.openai.com/en/articles/8590148-memory-faq) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, configuration templates, and scaffolded workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a local context workspace, typed memory objects, governance and evaluation documents, bundle manifests, and MCP server scaffolding.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
