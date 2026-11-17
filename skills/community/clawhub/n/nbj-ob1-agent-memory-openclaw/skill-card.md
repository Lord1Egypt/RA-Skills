## Description:

Use Nate Jones OB1 Agent Memory from OpenClaw with provenance, scope, review, and use-policy discipline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[natebjones](https://clawhub.ai/user/natebjones)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide OpenClaw agents through scoped OB1 memory recall, usage reporting, and compact write-back after meaningful work. It is especially useful for code review and long-running TaskFlow work where agents need continuity without storing transcripts or private data dumps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can cross project, tenant, or sensitivity boundaries if the OB1 service is not enforcing scope controls.

Mitigation: Confirm project and tenant boundaries before using the skill on sensitive work, prefer project-scoped recall, and keep project_only true by default.

Risk: Unreviewed or model-generated memories can become hidden instructions in later tasks.

Mitigation: Respect use_policy labels, require confirmation before relying on memories marked requires_user_confirmation, and keep agent-written memory as evidence until human-confirmed or imported from a trusted source.

Risk: Write-back can expose secrets, private customer data, or excessive task detail.

Mitigation: Write only compact summaries with provenance and source references, and do not store raw transcripts, reasoning traces, credential-like values, large code blocks, or private data dumps.

## Reference(s):

- [NBJ OB1 Agent Memory for OpenClaw integration](../../integrations/openclaw-agent-memory/)
- [OB1 Agent Memory API](../../integrations/agent-memory-api/)
- [NBJ OB1 Agent Memory for OpenClaw recipe](../../recipes/openclaw-agent-memory/)
- [OpenClaw Code Review Memory recipe](../../recipes/openclaw-code-review-memory/)
- [OpenClaw TaskFlow Work Log recipe](../../recipes/openclaw-taskflow-work-log/)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions]

**Output Format:** [Markdown instructions for agent memory recall, usage reporting, and write-back]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OB1/OpenBrain memory tools to perform recall, write-back, inspection, review queue, and recall trace operations; agents continue normally and disclose that no memory operation occurred when those tools are unavailable.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
