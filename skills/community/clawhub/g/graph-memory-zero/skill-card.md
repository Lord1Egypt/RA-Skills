## Description:

Production playbook for OpenClaw graph-memory optimization with mem0-aligned recall governance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyangwjy](https://clawhub.ai/user/wangyangwjy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to tune, verify, troubleshoot, and roll back OpenClaw graph-memory recall settings for production workspaces. It guides threshold, inference, memory-type filtering, and preference lexicon changes while preserving observability and rollback notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to patch graph-memory recall settings and restart OpenClaw during verification.

Mitigation: Confirm the schema path exists, snapshot current values and baseHash, apply only the smallest scoped patch, then verify live config and keep a one-step rollback path.

Risk: The documented SiliconFlow model and embedding endpoint may be used with workspace data.

Mitigation: Confirm the endpoint, model provider, data handling, and deployment region are approved for the workspace before applying the playbook.

## Reference(s):

- [Graph Memory Zero ClawHub Page](https://clawhub.ai/wangyangwjy/skills/graph-memory-zero)
- [Current Baseline](references/current-baseline.md)
- [Baseline Profiles](references/baseline-profiles.md)
- [Verification Playbook](references/verification-playbook.md)
- [Troubleshooting Matrix](references/troubleshooting.md)
- [Install Channels](references/install-channels.md)
- [SiliconFlow API Endpoint](https://api.siliconflow.cn/v1)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Markdown]

**Output Format:** [Markdown with inline configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes verification results and rollback information before claiming completion.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
