## Description:

Memory Core gives OpenClaw agents LanceDB-backed long-term memory storage and retrieval with intent and scene isolation to reduce unrelated memory contamination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilei0311](https://clawhub.ai/user/lilei0311)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to add persistent memory operations to OpenClaw agents, including ingesting remembered facts, retrieving scene-filtered memories, and deleting stored memories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved memories and retrieval queries may be sent to SiliconFlow or another configured embedding provider.

Mitigation: Use Ollama or local_mock for local-only embedding when appropriate, and avoid storing secrets or highly sensitive personal data.

Risk: Persistent local memory can retain sensitive or stale information across sessions.

Mitigation: Review the local LanceDB storage location, restrict local file access, and use the forget command to delete memories that should not persist.

Risk: The skill can reuse an existing SiliconFlow API key from ~/.openclaw/openclaw.json.

Mitigation: Confirm that automatic credential reuse is acceptable for the environment, or configure an explicit embedding provider and key policy before use.

## Reference(s):

- [Memory Core ClawHub skill page](https://clawhub.ai/lilei0311/skills/memory-core)

## Skill Output:

**Output Type(s):** [json, text, configuration]

**Output Format:** [JSON command responses containing memory IDs, status values, tags, retrieved memory text, scenes, scores, and truncation flags.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates a local LanceDB memory store; retrieval uses agent and scene filtering plus configurable result, score, and character budgets.]

## Skill Version(s):

0.1.3 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
