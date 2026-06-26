## Description: <br>
Openclaw Memory Transfer helps agents migrate user memories, preferences, writing style, and tool preferences from other AI assistants into OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myclaw-ai](https://clawhub.ai/user/myclaw-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agents use this skill to bring profile details, communication preferences, project context, tool preferences, and long-term memory from ChatGPT, Claude, Gemini, Copilot, Perplexity, Cursor, Windsurf, and related assistants into OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process sensitive assistant history, including personal, business, or third-party information. <br>
Mitigation: Review and redact imported data before writing it to OpenClaw memory, and require user confirmation before migration is finalized. <br>
Risk: Local-agent migration can read broad assistant files and directories if used without clear scope. <br>
Mitigation: Ask the agent to list exact files and directories before reading them, and avoid broad home-directory scans unless the user explicitly approves the scope. <br>
Risk: Full ChatGPT ZIP exports can contain more data than the user intends to migrate. <br>
Mitigation: Treat ZIP output as sensitive, inspect the migration preview, and skip credentials, secrets, and irrelevant historical content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/myclaw-ai/openclaw-memory-transfer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with optional JSON parser output and memory-file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user review and confirmation before imported memory is written.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
