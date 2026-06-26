## Description: <br>
Brain-like local memory plugin for OpenClaw that stores, searches, and injects memories with importance scoring, entity extraction, and automatic consolidation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flexrox](https://clawhub.ai/user/flexrox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this plugin to give OpenClaw agents persistent local memory for saving, searching, recalling, and managing conversation-derived memories across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation content, including credential-like or personal details, may be saved automatically and reused in future prompts. <br>
Mitigation: Disable auto-capture or auto-recall before sensitive work, and use the forget or wipe tools to remove sensitive memories. <br>
Risk: Local memory files persist on disk and may outlive the conversation where they were captured. <br>
Mitigation: Limit stored content, prune or wipe memories when needed, and protect the local account and storage used for ~/.openclaw/memory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flexrox/openclaw-local-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Plain text and Markdown memory summaries injected into context or returned by tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local JSON memory files under ~/.openclaw/memory; recall output is limited by configured result and context budgets.] <br>

## Skill Version(s): <br>
0.4.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
