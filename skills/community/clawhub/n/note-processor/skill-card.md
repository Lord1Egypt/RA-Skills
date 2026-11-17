## Description:

Summarize and analyze research notes created by research-assistant, including topic summaries, keyword extraction, topic search, and topic listing for the research_db.json format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johstracke](https://clawhub.ai/user/johstracke)

### License/Terms of Use:


## Use Case:

Developers and researchers use this skill to review accumulated research notes, identify recurring themes, and find topic-specific information without rereading every note. It is intended for local note analysis against the research-assistant database format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Terminal output may expose local note contents, tags, previews, and derived keywords from research_db.json.

Mitigation: Run only in trusted terminals and avoid shared logs when notes contain sensitive information.

Risk: Keyword extraction and key point detection are simple frequency- and pattern-based aids, not semantic analysis.

Mitigation: Use the output to guide review and confirm important conclusions against the underlying notes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/johstracke/skills/note-processor)
- [Publisher Profile](https://clawhub.ai/user/johstracke)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Terminal text with markdown-style examples and inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a local research_db.json file and prints summaries, keyword counts, search results, and topic lists.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
