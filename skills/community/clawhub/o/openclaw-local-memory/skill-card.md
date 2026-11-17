## Description:

Brain-like local memory plugin for OpenClaw that stores, searches, and injects memories with importance scoring, entity extraction, and automatic consolidation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flexrox](https://clawhub.ai/user/flexrox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to give an agent persistent local memory across sessions, including automatic capture, semantic recall, profile building, manual memory management, and memory cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation content can be automatically captured and later recalled, including sensitive information if users discuss it while the skill is enabled.

Mitigation: Disable autoCapture and autoRecall for sensitive work, avoid sharing credentials or secrets, and periodically review or wipe stored memories.

Risk: Persistent local memory can mix unrelated projects or users if the same memory namespace is reused.

Mitigation: Use separate containerTag values for different projects, users, or work contexts.

Risk: Stored memories may become outdated, incorrect, or overrepresented in future context.

Mitigation: Use local_memory_forget or local_memory_wipe to remove stale memories, and tune pruning, decay, and significance settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flexrox/skills/openclaw-local-memory)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Plain text and Markdown memory snippets returned by tools or injected into agent context]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Memory recall is locally generated and bounded by configuration such as max recall results, max memory injections, and context budget.]

## Skill Version(s):

0.4.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
