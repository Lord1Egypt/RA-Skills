## Description:

Get live Premier League football scores, goal scorers, bookings, and broadcast channels via ESPN API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stigg86](https://clawhub.ai/user/stigg86)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer questions about current or recent English Premier League scores, scorers, bookings, and US broadcast channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the skill contacts ESPN, which receives normal request metadata such as IP address and User-Agent.

Mitigation: Run only in environments where outbound requests to ESPN are acceptable.

Risk: Scores, bookings, and broadcast data depend on ESPN availability and update frequency.

Mitigation: Treat results as live third-party sports data and re-run or verify with an official source when accuracy is critical.

## Reference(s):

- [Premier League Scores Skill Page](https://clawhub.ai/stigg86/skills/pl-scores)
- [stigg86 Publisher Profile](https://clawhub.ai/user/stigg86)
- [ESPN Premier League Scoreboard API](https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text scores and event summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public ESPN data at runtime and prints results locally.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
