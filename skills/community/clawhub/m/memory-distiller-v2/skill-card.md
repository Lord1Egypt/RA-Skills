## Description: <br>
记忆蒸馏器 helps agents compress AI agent logs, long conversations, retrospectives, decisions, and memory files into structured summaries with source markers for later review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to distill daily logs, long conversation history, project retrospectives, decisions, action items, and memory archives into compact Markdown memory summaries. It is intended for local log and memory maintenance workflows where the user selects the files to process and reviews the result before appending it to persistent memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist private logs, chat history, credentials, customer data, or confidential work into long-lived memory files. <br>
Mitigation: Run it only on intentionally selected files, redact sensitive content first, and review the compressed output before appending it to MEMORY.md. <br>
Risk: The workflow relies on an unspecified local Node.js compression script and shell commands. <br>
Mitigation: Inspect or provide the actual memory-compress.js script before allowing exec, and run it in a local workspace with backups of the source logs. <br>
Risk: The archival workflow may move original logs after compression, making mistakes harder to recover from. <br>
Mitigation: Prefer copy-and-backup archival steps until the summary, source markers, and retained details have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/memory-distiller-v2) <br>
- [Node.js runtime](https://nodejs.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with source markers and optional shell commands for local compression workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append compressed summaries to MEMORY.md and may move original logs when the user follows the archival workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
