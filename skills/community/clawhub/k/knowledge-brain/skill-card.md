## Description:

Capture, summarize, and organize knowledge from URLs, YouTube videos, documents, and files. Proactively recall stored knowledge when relevant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plc](https://clawhub.ai/user/plc)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to maintain a personal knowledge base, generate summaries from captured sources, organize entries into categories, and recall saved knowledge during later conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill maintains a persistent local knowledge index that may summarize or expose private material across sessions.

Mitigation: Review what is stored in agent memory, keep sensitive sources out of the knowledge base, and use explicit recall commands when proactive search is not desired.

Risk: Proactive recall can search saved material across broad conversations and surface context that was not explicitly requested.

Mitigation: Limit activation to relevant conversations, inspect recalled entries before relying on them, and disable or narrow proactive recall for sensitive workflows.

Risk: Shell-command templates use user-supplied URLs, paths, and category names.

Mitigation: Quote and validate all user-provided values, avoid untrusted filenames or directory names, and harden command steps before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/plc/skills/knowledge-brain)
- [Artifact README](artifact/README.md)
- [Artifact Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown files, concise conversational summaries, and inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains paired raw and summary files, category notes, changelog entries, a lightweight memory index, and optional git commits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
