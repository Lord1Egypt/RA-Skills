## Description:

Distill successful multi-step OpenClaw sessions into reusable learned skills before compaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaocaijic](https://clawhub.ai/user/xiaocaijic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill after successful multi-step OpenClaw work to preserve reusable procedures, commands, file paths, snippets, and failure triggers as learned skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Past session traces may contain secrets, private code, internal paths, unsafe commands, or instruction-like content that would become persistent future guidance.

Mitigation: Review traces and generated learned skills before reuse, and remove sensitive or unsafe content before enabling long-term memory.

Risk: Generated procedures may preserve obsolete commands or failed assumptions from a specific environment.

Mitigation: Constrain the output directory, prefer traces explicitly approved for long-term memory, and validate generated skills in the target environment before relying on them.

## Reference(s):

- [Trace Format](artifact/references/trace-format.md)
- [ClawHub Skill Page](https://clawhub.ai/xiaocaijic/skills/procedural-distiller)
- [Publisher Profile](https://clawhub.ai/user/xiaocaijic)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, JSON, Files, Shell commands, Guidance]

**Output Format:** [Generated learned skill directory containing SKILL.md, agents/openai.yaml, and memory.json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May skip output when the trace is unsuccessful, has fewer than the configured minimum tool calls, or lacks enough detail to reconstruct a reusable procedure.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
