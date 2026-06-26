## Description: <br>
Manages multiple independent work windows for an agent, saving and restoring local progress and conversation context during window switches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[philonis](https://clawhub.ai/user/philonis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to organize separate work streams as named windows, resume prior progress, list or query windows, and mark work complete. It is intended for local workflow continuity where persisted conversation history is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local conversation transcripts may include secrets or confidential work and are saved for later reuse. <br>
Mitigation: Install only when transcript persistence is desired, avoid using it around sensitive material, and manage or delete files under ~/.openclaw/workspace/memory/tasks as needed. <br>
Risk: Switching windows may copy the latest local session rather than a session definitively tied to the window being left. <br>
Mitigation: Verify the active window and review restored history after switching before relying on it for context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/philonis/multi-windows) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown/text status responses plus local JSON, Markdown, and JSONL files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists window state, summaries, and transcript history under ~/.openclaw/workspace/memory/tasks.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
