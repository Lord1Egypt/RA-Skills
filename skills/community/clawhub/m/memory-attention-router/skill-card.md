## Description: <br>
Deterministic long-term memory routing for OpenClaw that routes, writes, reflects on, and refreshes reusable memory for multi-step agent work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiqiangh](https://clawhub.ai/user/kaiqiangh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to turn long-term local memory into compact, role-aware working-memory packets and to store, replace, or retire reusable memories after important outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist durable local memories that may later be surfaced in agent context. <br>
Mitigation: Do not store secrets, credentials, private customer data, or sensitive personal details; inspect saved memories periodically. <br>
Risk: Memory writes, replacements, or deletions can change future agent behavior. <br>
Mitigation: Require explicit approval for write, replacement, refresh, and deletion operations. <br>
Risk: A database path may place long-lived memory in an unexpected location. <br>
Mitigation: Check where MAR_DB_PATH points before use and keep the memory database in an appropriate local workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kaiqiangh/memory-attention-router) <br>
- [Reference guide](references/REFERENCE.md) <br>
- [Memory schema](references/MEMORY_SCHEMA.md) <br>
- [Prompt templates](references/PROMPTS.md) <br>
- [Testing guide](references/TESTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payload examples and shell commands; router script commands emit JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces compact working-memory packets with capped lists for selected memories, hard constraints, relevant facts, procedures, pitfalls, and open questions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
