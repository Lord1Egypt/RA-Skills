## Description:

Adds intelligent long-term memory to agents for auto-capturing, recalling, and managing user facts and preferences across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xray2016](https://clawhub.ai/user/xray2016)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and agent operators use this skill to add Mem0-backed memory to OpenClaw agents, including automatic recall before turns, automatic capture after turns, and manual memory management tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can automatically store sensitive chat content.

Mitigation: Disable autoCapture by default when sensitive conversations are possible, define clear capture rules, and avoid sharing sensitive data while capture is enabled.

Risk: Remote or cross-user memory access can expose recalled information if endpoints, credentials, or user scoping are misconfigured.

Mitigation: Use a trusted HTTPS Mem0 endpoint or controlled self-hosted backend, and scope backend credentials and user IDs per user or tenant.

Risk: Automatic recall may inject outdated, irrelevant, or inappropriate memories into the agent context.

Mitigation: Tune recall thresholds and top-k settings, review stored memories regularly, and disable autoRecall where context injection needs human control.

Risk: Memory deletion can remove records by explicit ID or by a high-confidence query match.

Mitigation: Review deletion behavior before deployment and prefer explicit memory IDs or an operator confirmation step for deletion workflows.

Risk: The security review guidance identifies dependencies that should be upgraded.

Mitigation: Upgrade flagged dependencies and re-run security review before broad deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/xray2016/skills/openclaw-mem0)
- [README.md](README.md)
- [Mem0](https://mem0.ai)
- [Mem0 project reference](https://github.com/mem0ai/mem0)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands, guidance]

**Output Format:** [Text responses with structured tool details, Markdown documentation, shell commands, and JSON configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides memory search, storage, retrieval, listing, and deletion outputs scoped by user or session.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
