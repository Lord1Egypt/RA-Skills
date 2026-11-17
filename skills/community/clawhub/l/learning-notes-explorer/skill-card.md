## Description:

Learning Notes Explorer helps agents search, retrieve, synthesize, and connect personal learning notes for review, gap analysis, and study guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Users with personal learning notes use this skill to search by keyword, topic, tag, or source, then synthesize summaries, identify connections and gaps, and generate learning paths. It is suited for personal knowledge review where the configured note collection is appropriate for agent access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill searches and summarizes personal learning notes that may contain private or sensitive information.

Mitigation: Configure the note path to a limited collection that is appropriate for agent access, and review generated summaries before sharing them.

Risk: Broad note-related prompts may activate the skill and surface more note content than intended.

Mitigation: Use specific prompts for sensitive collections and keep high-sensitivity notes outside the configured note storage.

Risk: Search and synthesis quality depends on the completeness and richness of the underlying note collection.

Mitigation: Treat summaries and learning paths as review aids, and verify important conclusions against the source notes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/learning-notes-explorer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include note titles, sources, tags, previews, synthesized concepts, connections, and suggested next steps when available.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
