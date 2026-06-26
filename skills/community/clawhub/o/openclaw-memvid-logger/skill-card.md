## Description: <br>
Logs OpenClaw conversations and events to JSONL and Memvid files so agents can preserve and search long-term conversation context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stackBlock](https://clawhub.ai/user/stackBlock) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to maintain searchable long-term memory across user messages, assistant responses, sub-agent activity, tool results, and system events. It is suited for users who intentionally want broad conversation logging and accept the related privacy responsibilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent broad logging can capture sensitive prompts, assistant responses, tool outputs, file contents, and system events. <br>
Mitigation: Install only for intentional always-on memory use, keep JSONL and .mv2 files in protected locations, and review or delete stored logs regularly. <br>
Risk: API mode can send captured content to the Memvid cloud service. <br>
Mitigation: Use local free or monthly sharding mode for sensitive work, or enable API mode only after accepting third-party processing. <br>
Risk: Configuring MEMVID_BIN, MEMVID_PATH, or JSONL_LOG_PATH to untrusted locations can expose data or execute an unexpected Memvid binary. <br>
Mitigation: Set these environment variables only to paths and binaries under your control. <br>
Risk: The skill does not provide built-in scope, redaction, or retention controls. <br>
Mitigation: Limit deployment to environments where complete conversation memory is acceptable, and manage retention externally through file permissions, rotation, and deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stackBlock/openclaw-memvid-logger) <br>
- [Memvid documentation](https://memvid.com/docs) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and environment variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local JSONL logs and Memvid .mv2 memory files when installed; API mode can send data to memvid.com.] <br>

## Skill Version(s): <br>
1.2.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
