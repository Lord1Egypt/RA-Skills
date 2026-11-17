## Description:

ProcessOn Mindmap Generator helps agents transform natural language, Markdown, long text, documents, webpages, and image text into structured, editable ProcessOn mind maps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leilizhang](https://clawhub.ai/user/leilizhang)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers can use this skill to summarize and reorganize source material into concise Markdown outlines for ProcessOn mind maps, including brainstorming maps, task breakdowns, problem analysis, study notes, meeting summaries, timelines, tree diagrams, and organization charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends mind-map source text to ProcessOn's cloud service.

Mitigation: Use it only with content approved for that data flow; avoid confidential, regulated, or proprietary material unless organizational policy allows the upload.

Risk: A persistent local partner identifier may correlate skill usage.

Mitigation: Review whether that tracking is acceptable before deployment and manage or remove the local ProcessOn partner identifier according to endpoint policy.

Risk: The skill includes automatic update instructions that install from an unpinned remote source.

Mitigation: Review the exact source version before accepting updates and prefer pinned, reviewed releases in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leilizhang/skills/processon-mindmap-generator)
- [ClawHub publisher profile](https://clawhub.ai/user/leilizhang)
- [ProcessOn skills repository referenced by README](https://github.com/processonai/processon-skills/tree/main/skills/processon-mindmap-generator)
- [ProcessOn Markdown transform API used by client](https://smart.processon.com/v1/api/transform/md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown mind-map outline with ProcessOn online view and image URLs; shell commands may be used for installation, updates, and API submission.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports seven ProcessOn structures: mind_free, mind_right, mind_org, mind_ishikawa_left, mind_timeline_h, mind_tree_free, and mind_treeTable_left_title.]

## Skill Version(s):

1.1.10 (source: frontmatter, release evidence, version files)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
