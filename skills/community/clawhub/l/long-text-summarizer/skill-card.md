## Description:

Long Text Summarizer helps agents summarize long or ultra-long documents with a Map/Reduce and hierarchical reduction workflow, with controls for summary format, length, tone, and focus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other agent users use this skill to summarize papers, reports, books, chat logs, long webpages, and batches of documents that exceed a single model context window. It guides chunking, per-chunk summaries, and final reduction into a structured summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The learner component can persist usage notes, errors, and preferences beyond the immediate summarization task.

Mitigation: Avoid using the learner component with sensitive documents or confidential workflow details unless local plaintext history is acceptable and managed.

Risk: Long-document Map/Reduce summarization can lose cross-chunk themes or accumulate early errors.

Mitigation: Use hierarchical reduction for very long inputs, preserve chunk references, and review the final summary against source chunks for important decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/long-text-summarizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with prompt templates, bash commands, and optional JSON chunk files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable summary format, length, tone, focus, chunk size, and overlap.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
