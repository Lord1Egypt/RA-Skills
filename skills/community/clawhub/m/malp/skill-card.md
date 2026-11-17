## Description:

MALP helps agents scout, create, refresh, classify, and use project-local `.malp/` context notes for development work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inertia186](https://clawhub.ai/user/inertia186)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use MALP to preserve lightweight local project context, choose the right context notes for a task, and maintain active, attic, or unindexed `.malp/` states without loading unnecessary material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MALP can create persistent `.malp/` directories in target projects and maps under `~/.malp-home/`.

Mitigation: Use it only when the user intent identifies the target, and decide whether `.malp/` files should be ignored, left untracked, or committed for each repository.

Risk: Project notes may accidentally capture secrets or sensitive local context.

Mitigation: Keep credentials and secrets out of `.malp/` notes, and review notes before sharing or committing them.

Risk: Optional Kino scouting can read repository structure and shallow git metadata for recommendations.

Mitigation: Use git-history options only when they materially help the task, and treat Kino output as provisional context rather than authority.

## Reference(s):

- [MALP Skill Page](https://clawhub.ai/inertia186/skills/malp)
- [Operational tasks and file conventions](references/tasks.md)
- [Active, attic, and unindexed states](references/indexing.md)
- [Attic archive behavior](references/attic.md)
- [Repository strategies for `.malp/`](references/repo-strategies.md)
- [Clawpatch-aware MALP workflow](references/clawpatch.md)
- [Kino scout helper](scripts/kino.py)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown responses with optional shell commands, JSON scout output, and plain-text `.malp` note files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project-local `.malp/` files and user-level MALP map files only when the user intent covers the target.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
