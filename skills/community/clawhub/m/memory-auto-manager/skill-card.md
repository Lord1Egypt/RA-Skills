## Description: <br>
Automatically manages memory based on built-in memory-lancedb-local-storage by extracting key points, compressing conversations, writing to MEMORY.md, and updating the vector index after sessions end. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuchuanyu1](https://clawhub.ai/user/xuchuanyu1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to automatically summarize completed conversations into durable memory entries and refresh the local vector memory index. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Completed conversations may be sent to the configured LLM and persisted into long-term memory without review. <br>
Mitigation: Use only in workspaces where automatic summarization is acceptable, and add review or approval before memory entries are retained. <br>
Risk: Sensitive, private, regulated, credential-bearing, or confidential content can be captured in MEMORY.md and indexed for later retrieval. <br>
Mitigation: Avoid using the skill for sensitive work unless redaction, disable, and deletion controls are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuchuanyu1/memory-auto-manager) <br>
- [Publisher profile](https://clawhub.ai/user/xuchuanyu1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown memory entries appended to MEMORY.md with a vector index update command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs automatically on session-end and /new hooks, with a manual process-all command and daily scheduled processing when cron support is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
