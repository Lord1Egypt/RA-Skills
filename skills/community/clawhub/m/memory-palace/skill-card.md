## Description: <br>
Memory Palace provides persistent memory management for agents, including user preferences, project state, reusable experience records, semantic search, and time reasoning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanzhou3](https://clawhub.ai/user/lanzhou3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to give an agent long-lived local memory for user preferences, project context, technical decisions, and reusable lessons. It is most relevant when the agent should recall prior interactions or search stored memories across time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently stores personal data and project context in local memory files. <br>
Mitigation: Use it only for information intended to be retained, avoid secrets or regulated personal data, and periodically audit and delete stored memories. <br>
Risk: LLM-enhanced features can send stored memory content to the configured model provider. <br>
Mitigation: Review the configured provider and consent model before enabling these features, or disable them with MEMORY_PALACE_DISABLE_LLM=true when memory contents should remain local. <br>
Risk: Security guidance identifies memory ID path validation as a required fix before untrusted tool arguments are allowed. <br>
Mitigation: Restrict use to trusted agent calls and local workspaces until memory IDs are validated and constrained to the intended storage directory. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lanzhou3/memory-palace) <br>
- [API Reference](references/api-reference.md) <br>
- [Architecture](references/architecture.md) <br>
- [Usage Examples](references/usage-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON-like tool arguments, shell commands, and structured text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill stores and retrieves local memory records, can emit summaries or search results, and may use optional LLM and vector-search integrations when configured.] <br>

## Skill Version(s): <br>
1.8.5 (source: package.json and changelog, released 2026-04-08) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
