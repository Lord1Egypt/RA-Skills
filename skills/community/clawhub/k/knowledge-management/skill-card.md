## Description:

Organize and classify OpenClaw knowledge entries into local folders by content type (Research, Decision, Insight, Lesson, Pattern, Project, Reference, Tutorial).

This skill is ready for commercial/non-commercial use.

## Publisher:

[claireaicodes](https://clawhub.ai/user/claireaicodes)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to organize local memory entries into a structured markdown knowledge base, classify entries by content type and metadata, generate indexes, and manage synced knowledge files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Index generation can execute JavaScript while parsing markdown metadata.

Mitigation: Run `km summarize` only on trusted workspace content or in a dedicated test workspace until metadata parsing is replaced with a non-executing parser.

Risk: Cleanup can permanently delete local knowledge files identified as orphaned.

Mitigation: Use dry-run cleanup first, keep recoverable backups, and avoid scheduled cleanup until deletion requires confirmation or uses archive/quarantine.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/claireaicodes/skills/knowledge-management)
- [Publisher Profile](https://clawhub.ai/user/claireaicodes)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown files, JSON command output, and CLI-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes organized local knowledge files and index files under the configured workspace/output directory.]

## Skill Version(s):

2.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
