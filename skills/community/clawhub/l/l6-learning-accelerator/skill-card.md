## Description:

Provides time-aware memory retrieval by combining vector similarity with temporal relevance and tracks learning progress for study workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wyblhl](https://clawhub.ai/user/wyblhl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to rank learning notes or memory items by vector similarity and temporal relevance, parse time-related study queries, and generate progress reports for learning sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Progress import/export functions accept caller-provided file paths and may read from or overwrite arbitrary local paths.

Mitigation: Allow only trusted callers to choose paths, restrict import/export to a dedicated progress-data directory, and prevent silent overwrites.

Risk: Imported progress JSON can replace in-memory sessions and milestones without schema or size checks.

Mitigation: Validate imported JSON structure and size before loading it into a workspace or agent runtime.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wyblhl/skills/l6-learning-accelerator)
- [Publisher profile](https://clawhub.ai/user/wyblhl)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript code examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ranked retrieval results, temporal date ranges, and progress report objects when its JavaScript APIs are used.]

## Skill Version(s):

1.0.0 (source: server release metadata; README version agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
