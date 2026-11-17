## Description:

Maoyan CLI helps agents query Maoyan cinema schedules, search movies, find cinemas, and retrieve movie details through a local Python CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[island-x](https://clawhub.ai/user/island-x)

### License/Terms of Use:


## Use Case:

External users, developers, and agent operators use this skill to answer cinema and movie availability questions from Maoyan data, including city lookup, cinema listings, showtimes, movie search, cinema availability for a movie, and movie details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Python script that contacts Maoyan endpoints.

Mitigation: Review proposed commands before execution and use the skill only in environments where outbound requests to Maoyan are acceptable.

Risk: Optional latitude and longitude parameters can send precise location data to Maoyan for distance-based cinema results.

Mitigation: Omit precise coordinates unless distance sorting is needed and the user has provided or approved that location use.

## Reference(s):

- [Maoyan CLI reference](reference.md)
- [Maoyan CLI examples](examples.md)
- [Maoyan mobile site](https://m.maoyan.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The invoked CLI commands output structured JSON for agent parsing.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
