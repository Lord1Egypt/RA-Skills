## Description: <br>
Enable and configure Moltbot/Clawdbot memory search for persistent context, including MEMORY.md, daily logs, and vector search setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jackwang2999](https://clawhub.ai/user/Jackwang2999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure persistent memory search for Moltbot/Clawdbot workspaces, create memory file structure, and troubleshoot recall behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory search can index past conversation transcripts and personal workspace context. <br>
Mitigation: Review which sources are enabled, avoid storing secrets or regulated data in memory files, and only index transcripts that are appropriate for the workspace. <br>
Risk: External embedding providers may process memory content when configured. <br>
Mitigation: Prefer the local provider for sensitive workspaces, or review provider data handling before enabling Voyage or OpenAI embeddings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jackwang2999/memory-setup-jack) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration instructions, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with JSON, markdown, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance for configuring memory search and memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
