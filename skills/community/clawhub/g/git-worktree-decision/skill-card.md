## Description:

Helps developers decide whether concurrent work, an occupied checkout, or side-by-side comparison warrants a separate Git worktree.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to decide when to create a separate Git worktree, check for shared resources that could make parallel work unsafe, and plan when to remove the worktree.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Worktree removal or pruning can affect local checkout state.

Mitigation: Review worktree commands and check for uncommitted changes before running removal or prune commands.

Risk: Parallel worktrees can conflict over shared ports, databases, containers, or other external state.

Mitigation: Identify and separate shared resources before working concurrently, or sequence the work instead.

## Reference(s):

- [git-worktree-decision on ClawHub](https://clawhub.ai/clarezoe/skills/git-worktree-decision)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown text with inline Git commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Decision criteria and cleanup guidance; no automatic command execution.]

## Skill Version(s):

1.0.1 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
