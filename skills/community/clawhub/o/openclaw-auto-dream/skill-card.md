## Description: <br>
Openclaw Auto Dream helps OpenClaw agents consolidate daily logs into structured long-term memory with importance scoring, insight reports, dashboard updates, and notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myclaw-ai](https://clawhub.ai/user/myclaw-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to run scheduled or manual memory consolidation that turns workspace daily logs into long-term memory, procedural notes, episodic records, archive entries, and status reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists and restructures potentially sensitive memory content from MEMORY.md and memory/ logs. <br>
Mitigation: Review or redact sensitive entries before installation, keep notification channels private, and install only when a scheduled memory job is desired. <br>
Risk: Generated dashboards and migration bundles can expose or carry private memory content. <br>
Mitigation: Sanitize memory content before opening dashboards or sharing exports, and import only bundles the user explicitly selected and trusts. <br>
Risk: Automated consolidation changes long-term memory files and indexes. <br>
Mitigation: Use the skill's documented backup behavior for large MEMORY.md changes, index updates, and imports, and review dream reports after consolidation. <br>


## Reference(s): <br>
- [Openclaw Auto Dream on ClawHub](https://clawhub.ai/myclaw-ai/openclaw-auto-dream) <br>
- [MyClaw.ai](https://myclaw.ai) <br>
- [Auto-Dream Lite - Quick Memory Consolidation](references/dream-prompt-lite.md) <br>
- [Auto-Dream Cycle - Execution Prompt v3.0](references/dream-prompt.md) <br>
- [First Dream - Post-Install Memory Scan](references/first-dream-prompt.md) <br>
- [Memory Templates v3.0](references/memory-template.md) <br>
- [Scoring and Forgetting - Memory Evaluation Algorithms v3.0](references/scoring.md) <br>
- [Cross-Instance Memory Migration v3.0](references/migration-cross-instance.md) <br>
- [Migration Guide v1 to v2](references/migration-v1-to-v2.md) <br>
- [Migration Guide v1 to v2 to v3](references/migration-v2-to-v3.md) <br>
- [Dashboard Template](references/dashboard-template.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands, configuration snippets, and generated memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append or update MEMORY.md and files under memory/ when the agent follows the skill workflow.] <br>

## Skill Version(s): <br>
4.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
