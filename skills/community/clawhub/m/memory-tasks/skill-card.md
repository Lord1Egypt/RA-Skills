## Description:

Task management via Basic Memory schemas: create, track, and resume structured tasks that survive context compaction. Uses BM's schema system for uniform notes queryable through the knowledge graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phernandez](https://clawhub.ai/user/phernandez)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create, track, query, update, and close persistent task notes for multi-step work that may need to resume after context compaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent task notes may retain sensitive or private details across sessions.

Mitigation: Keep task notes concise, avoid secrets and private customer data, and install only when persistent Basic Memory task state is desired.

Risk: Outdated active tasks can mislead future resumption work.

Mitigation: Update progress before compaction and periodically close or remove tasks that no longer need to be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phernandez/skills/memory-tasks)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance]

**Output Format:** [Markdown task notes with YAML frontmatter, structured checklist content, and concise operational guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to be stored as Basic Memory task records and kept current as work progresses.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
