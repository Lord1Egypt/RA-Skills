## Description: <br>
Transfer memory files between OpenClaw agents with support for topic-specific transfers and two modes: memory sharing with role transformation and memory cloning as a verbatim copy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeblackhole1024](https://clawhub.ai/user/codeblackhole1024) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to inspect, search, preview, and transfer persistent memory files between OpenClaw agent workspaces for migration, backup, or topic-scoped knowledge sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move persistent agent memory between local OpenClaw workspaces, including private context in clone mode. <br>
Mitigation: Use dry-run first, prefer topic or file scoped transfers, and avoid clone mode for private data unless a full backup or migration is intentional. <br>
Risk: The documented confirmation safeguards are not reliably enforced by the artifact behavior. <br>
Mitigation: Manually verify the source agent ID, target agent ID, transfer mode, and selected files before executing a transfer. <br>
Risk: Share mode privacy filtering may be incomplete. <br>
Mitigation: Review transferred memory content before reuse and remove sensitive user information that pattern filtering did not catch. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codeblackhole1024/memory-transfer-enhanced) <br>
- [Publisher profile](https://clawhub.ai/user/codeblackhole1024) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Node.js file operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May preview transfers, list or search memories, and write or back up OpenClaw memory files when executed.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
