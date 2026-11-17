## Description:

External long-term memory and knowledge base backed by the MemOS Cloud API for searching, storing, correcting, deleting, profiling, and managing memory and knowledge base documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaohuisu](https://clawhub.ai/user/xiaohuisu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an agent to MemOS Cloud for long-term conversation memory, user profile retrieval, memory correction or deletion, and knowledge base document management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation history may be sent to and retained by MemOS Cloud by default.

Mitigation: Install only when external long-term memory storage is intended, and avoid entering secrets or sensitive content while the skill is active.

Risk: Incorrect endpoint or credential configuration can send memory data to an unintended service or tenant.

Mitigation: Configure MEMOS_API_KEY, MEMOS_USER_ID, and any custom endpoint only in a trusted environment, and prefer a host-provided stable session ID.

Risk: Remote uploads, deletions, and memory feedback can change stored memory or knowledge base state.

Mitigation: Confirm upload and deletion actions before execution, especially for sensitive files, shared knowledge bases, or memory correction workflows.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/xiaohuisu/skills/memos-cloud-skill)
- [MemOS Cloud API Endpoint](https://memos.memtensor.cn/api/openmem/v1)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, json, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, MEMOS_API_KEY, and MEMOS_USER_ID; uses the configured MemOS Cloud endpoint for memory and knowledge base operations.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
