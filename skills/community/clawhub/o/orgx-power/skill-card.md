## Description:

Power-user OrgX skill for OpenClaw. Use when you explicitly need the full mutation surface for entity CRUD, run control, checkpoints, stream reassignment, or agent-config policy changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hopeatina](https://clawhub.ai/user/hopeatina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OrgX operators use this skill when they explicitly need elevated OpenClaw actions for direct entity mutation, run control, checkpoint restore, stream reassignment, or managed agent policy changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables administrator-level OrgX changes, including irreversible, org-wide, checkpoint, session, and agent configuration operations.

Mitigation: Install only for agents expected to perform OrgX administrator-level changes, require explicit approval for sensitive operations, and prefer the default orgx skill for routine work.

Risk: Elevated tools may be unavailable on domain-scoped managed OrgX surfaces.

Mitigation: Fall back to the safe orgx skill and request the necessary human decision or orchestration context when elevated tools are not exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hopeatina/skills/orgx-power)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown with inline JavaScript tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assumes the runtime exposes elevated OrgX tools; use the default-safe orgx skill when those tools are unavailable or when routine work does not require admin-level changes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
