## Description:

Learn from experience helps an agent record corrections, self-reflections, reusable preferences, and confirmed patterns in local memory files and sync selected learnings into agent global configuration for cross-session persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shibing624](https://clawhub.ai/user/shibing624)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to make an assistant retain explicit corrections, confirmed preferences, and reusable work patterns across sessions while keeping memory organized by global, domain, project, and archive tiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can change future agent behavior across sessions and supported agent products.

Mitigation: Install only when persistent learning is intended, keep memory local, and periodically review the stored memory files.

Risk: Global config sync may write learned preferences into automatically loaded agent configuration.

Mitigation: Require a visible diff and explicit approval before sync modifies any global config file, and limit changes to the documented Patterns block.

Risk: Optional companion skill installation could expand behavior beyond this skill.

Mitigation: Decline the companion skill unless its publisher, version, and files have been separately reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shibing624/skills/learn-from-experience)
- [SKILL.md](artifact/SKILL.md)
- [Setup guide](artifact/setup.md)
- [Memory operations](artifact/operations.md)
- [Security boundaries](artifact/boundaries.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory files and proposed or applied updates to agent configuration sections when sync is used.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
