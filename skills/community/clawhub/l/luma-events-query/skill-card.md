## Description:

Queries public Lu.ma/Luma events by city or keyword in the same style as the Luma app search box, including Chinese mainland city searches, without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diaoxiaoniu](https://clawhub.ai/user/diaoxiaoniu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to find recent public Luma events for a requested city or city-plus-topic query, then present concise event summaries with title, time, city or venue, host, and Lu.ma link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: City and optional topic searches are sent to Luma's public API.

Mitigation: Avoid entering sensitive private details in search terms and tell users when queries leave the local agent environment.

Risk: The alternate npx installer path is not version-pinned.

Mitigation: Prefer the OpenClaw install path for normal installation, or pin and review the source before using an alternate installer.

Risk: Event availability and venue details depend on Luma's public API response and may be incomplete or hidden until registration.

Mitigation: Present event results as public Luma data, include timezone and Lu.ma links, and note when the venue is visible only after registration.

## Reference(s):

- [Server-resolved source repository](https://github.com/diaoxiaoniu/luma-events-query)
- [ClawHub skill listing](https://clawhub.ai/diaoxiaoniu/skills/luma-events-query)
- [Publisher profile](https://clawhub.ai/user/diaoxiaoniu)
- [Luma public events](https://lu.ma)
- [Luma discover events API endpoint used by the skill](https://api.lu.ma/discover/get-paginated-events)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; the helper script returns JSON event data for the agent to summarize.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Event summaries should stay concise and include title, time with timezone, city or venue, host, and Lu.ma URL.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
