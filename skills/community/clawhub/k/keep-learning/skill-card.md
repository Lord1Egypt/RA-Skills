## Description:

Keep Learning helps an agent learn from local Markdown and code directories, extract key insights, build a knowledge index, and store summaries in memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nileader](https://clawhub.ai/user/nileader)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to have an agent scan a confirmed local knowledge base, update memory with key insights, and maintain an index for later lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read the selected local directory and retain extracted summaries or indexes in agent memory.

Mitigation: Confirm the knowledge base path before use and avoid directories containing secrets or private data that should not be remembered.

Risk: The skill can run git pull in a selected repository before scanning files.

Mitigation: Use reviewed repositories, prefer pinned releases or verified commits, and review repository changes before learning.

## Reference(s):

- [Memory Strategy Reference](references/MEMORY-STRATEGY.md)
- [Supported File Formats](references/SUPPORTED-FORMATS.md)
- [ClawHub Skill Page](https://clawhub.ai/nileader/skills/keep-learning)
- [Project Repository](https://github.com/nileader/keep-learning)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown learning report with memory and knowledge-index entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists learned summaries and indexes in agent memory after the user confirms the knowledge base path.]

## Skill Version(s):

0.0.2 (source: release evidence, frontmatter metadata, CHANGELOG released 2026-03-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
