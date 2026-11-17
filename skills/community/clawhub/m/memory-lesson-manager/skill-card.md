## Description:

Structured memory and skill extraction tool for recording errors, corrections, decisions, projects, and people, with HOT/WARM/COLD lesson tiers, state recovery, semantic search, diary linking, promotion, and archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tank2737](https://clawhub.ai/user/tank2737)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to maintain a local lesson memory system, capture reusable corrections and decisions, promote frequently used lessons, archive stale lessons, and extract repeated patterns into standalone skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled shell scripts create and modify local memory, diary, state, lesson, and skill files.

Mitigation: Run mutating commands with --dry-run where available, keep backups or version control, and review planned file changes before applying them.

Risk: The security scan reports unsafe shell patterns that can execute injected shell code or search outside the intended memory area.

Mitigation: Avoid untrusted environment variables and untrusted --type values until the reported eval and path traversal issues are fixed.

Risk: Migration and rollback procedures can move or delete existing memory and state files.

Mitigation: Back up the memory and template directories before migration, verify backups, and avoid rollback rm -rf commands unless the target paths have been reviewed.

## Reference(s):

- [Usage Guide](references/usage-guide.md)
- [Usage Examples](references/usage-examples.md)
- [Migration Guide](references/migration-guide.md)
- [Optimization Proposals](references/optimization-proposals.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and generated local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and updates local memory, diary, state, lesson, and skill files when mutating scripts are run.]

## Skill Version(s):

2.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
