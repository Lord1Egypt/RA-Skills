## Description: <br>
Persistent memory system for AI agents - daily logs, long-term memory, identity files, and heartbeat-driven recall. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[Clawdssen](https://clawhub.ai/user/Clawdssen) <br>

### License/Terms of Use: <br>
CC-BY-NC-4.0 <br>


## Use Case: <br>
Developers and AI-agent operators use Memory OS to install local workspace files that preserve agent identity, user context, long-term memory, daily notes, and optional proactive check templates across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory files can retain sensitive personal or work context that may be reused in later sessions. <br>
Mitigation: Install only in a private workspace and avoid storing secrets, credentials, regulated data, or anything the operator would not want reused later. <br>
Risk: Generated memory and identity files can influence future agent behavior. <br>
Mitigation: Review AGENTS.md, USER.md, MEMORY.md, HEARTBEAT.md, daily notes, and .blueprint-state.json after installation, and keep heartbeat, web research, email, and calendar checks disabled or narrowed unless explicitly needed. <br>


## Reference(s): <br>
- [Memory OS on ClawHub](https://clawhub.ai/Clawdssen/memory-os) <br>
- [Blueprint YAML](references/blueprint.yaml) <br>
- [Memory OS Guide](references/guide.md) <br>
- [The Agent Ledger](https://theagentledger.com) <br>
- [Skill-declared project URL](https://github.com/theagentledger/agent-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown instructions plus local Markdown and JSON workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or merges local workspace memory files after explicit operator confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
