## Description: <br>
Memory Distiller automatically distills conversation insights, corrections, and preferences into durable memory for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zcyynl](https://clawhub.ai/user/zcyynl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to help OpenClaw agents retain reusable corrections, preferences, and lessons from conversations without manually editing memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may silently save selected conversation details into long-term memory. <br>
Mitigation: Use it only when automatic memory is desired, and regularly inspect MEMORY.md, USER.md, and dated memory files for private, incorrect, or unwanted entries. <br>
Risk: Broad triggers may capture preferences, corrections, or insights that the user did not intend to persist. <br>
Mitigation: Avoid sensitive sessions with this skill enabled, and delete or edit unwanted entries after reviewing the memory files. <br>
Risk: Stored memories can influence future agent behavior if they are outdated or inaccurate. <br>
Mitigation: Keep the quality gate strict and update stale memory entries rather than duplicating them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zcyynl/memory-distiller) <br>
- [Claudeception inspiration](https://github.com/disler/claudeception) <br>
- [claw-multi-agent](https://github.com/zcyynl/claw-multi-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown memory entries written to MEMORY.md, USER.md, or memory/YYYY-MM-DD.md, with optional short text confirmation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Auto-triggered writes are silent; explicit memory requests receive a brief confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
