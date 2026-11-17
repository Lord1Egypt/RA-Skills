## Description:

Query Dutch field hockey match schedules and results from KNHB Match Center (hockeyweerelt.nl). Use when looking up hockey clubs, teams, upcoming matches, or match results in the Netherlands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tader](https://clawhub.ai/user/tader)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to look up Dutch field hockey clubs, teams, upcoming matches, played matches, scores, and venue details from the public KNHB Match Center API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides agents to make public API requests to hockeyweerelt.nl and process returned data locally.

Mitigation: Install only when KNHB or Dutch field hockey lookup is desired, and review generated curl and jq commands before execution.

Risk: Match schedules, scores, venues, and time conversions may be stale or misread if the public API response changes.

Mitigation: Use the live API response as the source of truth and convert UTC datetimes with a reliable local date tool or date library.

## Reference(s):

- [KNHB Match Center API base](https://publicaties.hockeyweerelt.nl/mc)
- [ClawHub skill page](https://clawhub.ai/tader/skills/knhm-match-center)
- [ClawHub publisher profile](https://clawhub.ai/user/tader)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and JSON response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl and jq examples for public KNHB Match Center API requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
