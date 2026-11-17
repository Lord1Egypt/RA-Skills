## Description:

Percept Summarize generates searchable conversation summaries with entity extraction, action items, and relationship mapping after a silence timeout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarvis563](https://clawhub.ai/user/jarvis563)

### License/Terms of Use:


## Use Case:

People using Percept use this skill to turn recent conversations and meetings into searchable summaries, action items, entity records, and relationship context for later retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes and stores sensitive conversation content, entities, relationships, and speaker profiles.

Mitigation: Review it before installation in private, regulated, or workplace settings; confirm user consent, data access controls, and deletion or expiration policies.

Risk: The security evidence notes unclear controls around external summarization through OpenClaw processing.

Mitigation: Confirm whether OpenClaw processing is local or remote and whether transcripts leave the intended environment before enabling automatic summarization.

Risk: Stored summaries and relationship data may be accessible through SQLite or the dashboard.

Mitigation: Restrict access to the SQLite database and dashboard, and verify retention settings for utterances, summaries, relationships, and speaker profiles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jarvis563/skills/percept-summarize)
- [Percept GitHub repository](https://github.com/GetPercept/percept)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Text summaries plus SQLite-backed conversation, entity, relationship, and action-item records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Searchable through the Percept dashboard on port 8960 or SQLite; retention varies by data type.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
