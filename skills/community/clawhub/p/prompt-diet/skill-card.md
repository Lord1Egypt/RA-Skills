## Description: <br>
Analyze and optimize OpenClaw system prompt token usage by auditing workspace prompt files, recommending safe compression opportunities, and applying approved changes with backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dgkim311](https://clawhub.ai/user/dgkim311) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit OpenClaw workspace prompt files, measure token usage, classify compression opportunities by safety tier, and apply only user-approved edits while preserving agent behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approved edits to prompt and memory files can change future agent behavior if important context is removed or rewritten. <br>
Mitigation: Review recommendations before applying them, never silently remove MEMORY.md entries, and keep generated backups until the result is confirmed. <br>
Risk: Token counts are estimates and may differ from the model's actual accounting. <br>
Mitigation: Treat savings as approximate and verify behavior after changes rather than optimizing solely for reported token totals. <br>


## Reference(s): <br>
- [Compression Rules](references/compression-rules.md) <br>
- [Token Count Script](scripts/token_count.py) <br>
- [ClawHub Skill Page](https://clawhub.ai/dgkim311/prompt-diet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, token-count tables or JSON, recommendation tables, shell commands, backup instructions, and before-and-after summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create backup files or backup directories before approved edits; token counts are estimates and may use tiktoken or a chars-per-token fallback.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
