## Description: <br>
A long-term memory management skill that helps an agent maintain local memory files, archive working context, track daily learning, and remind users about memory maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[konzenkane](https://clawhub.ai/user/konzenkane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to set up a persistent local memory workflow for an AI assistant, including MEMORY.md, session state, working-buffer archives, heartbeat checks, and daily learning logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local long-term memory files may accumulate personal, sensitive, or outdated information. <br>
Mitigation: Review MEMORY.md and memory/ files regularly, avoid storing secrets or highly sensitive personal data, and prune stale entries. <br>
Risk: Cron or autonomous learning examples can create scheduled local activity that users may forget is enabled. <br>
Mitigation: Enable scheduled jobs only after inspecting how they run, and document how to disable them. <br>


## Reference(s): <br>
- [龙虾记忆系统指南](references/memory-system-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/konzenkane/lobster-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and local file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory-management guidance and helper scripts; no API keys or MCP tools are required by the evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
