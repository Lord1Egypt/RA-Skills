## Description:

Personal Context Manager helps an agent capture personal reflections, imported information, knowledge connections, minimal-kernel summaries, cognitive maps, sprouts, and observer-style diary feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and productivity-focused users use this skill with an agent to record daily reflections, connect external information to personal judgments, and periodically refine a compact personal context kernel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create long-lived local records of sensitive personal reflections and imported conversations.

Mitigation: Redact secrets and third-party private information before saving content, and review where generated notes are stored and who can access them.

Risk: The entropy reduction script can delete user notes when run with force.

Mitigation: Run entropy reduction in dry-run mode first, review deletion candidates manually, keep backups, and use force only when deletion is intentional.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lj22503/skills/personal-context-manager)
- [Skill instructions](artifact/SKILL.md)
- [README](artifact/README.md)
- [Entropy reduction script](artifact/scripts/entropy_reduce.py)
- [Round 1 evaluation summary](artifact/evolve-test/round-1/summary.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown notes, structured local files, reports, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local data directories for journal, external information, core summaries, and connections; the entropy reduction script can update or delete local Markdown notes when explicitly run with force.]

## Skill Version(s):

2.0.0 (source: server release, skill frontmatter, and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
