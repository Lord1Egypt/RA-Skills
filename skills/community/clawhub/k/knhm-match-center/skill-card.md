## Description: <br>
Query Dutch field hockey match schedules and results from KNHB Match Center (hockeyweerelt.nl). Use when looking up hockey clubs, teams, upcoming matches, or match results in the Netherlands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tader](https://clawhub.ai/user/tader) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up Dutch field hockey clubs, teams, upcoming matches, locations, and played match results from the KNHB Match Center. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to a public KNHB Match Center API. <br>
Mitigation: Allow network access only when public match, club, and team lookups are intended. <br>
Risk: Match times are returned in UTC and may be misleading if presented without timezone conversion. <br>
Mitigation: Convert times with an appropriate date library or command before presenting local Amsterdam dates and times. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tader/knhm-match-center) <br>
- [KNHB Match Center API base](https://publicaties.hockeyweerelt.nl/mc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON response descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides read-only public API lookups and may include curl and jq examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
