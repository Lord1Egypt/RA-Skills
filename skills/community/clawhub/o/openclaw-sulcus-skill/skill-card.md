## Description:

Openclaw Sulcus Skill equips an agent with Sulcus memory, knowledge-graph recall, session memory, temporal supersession, and optional guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcdoolz](https://clawhub.ai/user/mcdoolz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent local or cloud-backed memory, automatic recall, session scratch-pad memory, and optional guardrails to an OpenClaw agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived memories, metadata, search queries, session events, and embedding requests can be persisted remotely when cloud mode is configured.

Mitigation: Prefer local-only mode for sensitive work, and use cloud mode only with a trusted Sulcus server, scoped API key, and appropriate namespace.

Risk: Automatic capture can store conversation content beyond the immediate session when enabled.

Mitigation: Keep autoCapture and captureFromAssistant disabled unless persistent capture is explicitly intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mcdoolz/skills/openclaw-sulcus-skill)
- [Sulcus](https://sulcus.ca)
- [Sulcus API endpoint](https://api.sulcus.ca)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides use of an OpenClaw plugin that can store and recall memory locally or through a configured Sulcus server.]

## Skill Version(s):

4.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
