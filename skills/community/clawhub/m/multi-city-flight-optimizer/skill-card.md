## Description:

Helps multi-city travelers collect trip constraints, compare outbound and return city combinations, rank the top itineraries by price, transfers, and travel time, and produce route suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[purelanren](https://clawhub.ai/user/purelanren)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers use this skill to evaluate multi-city flight options when destinations, dates, and preferences are flexible. It supports comparing all outbound and return city pairings, highlighting the top three choices, and generating a shareable HTML itinerary comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to run FlyAI commands with HTTPS certificate verification disabled.

Mitigation: Require normal TLS certificate validation and remove the TLS-bypass environment variable before running flight-search commands.

Risk: User-provided cities, dates, and preferences are passed into shell command examples.

Mitigation: Validate arguments, restrict them to expected values and formats, and pass them safely without shell interpolation.

Risk: The skill can generate shareable HTML itinerary files from dynamic travel data.

Mitigation: Escape generated HTML content and use only trusted HTTPS booking or reference links.

Risk: The skill may remember travel preferences or write itinerary details to files.

Mitigation: Confirm user consent before storing travel details in Memory or creating shareable HTML files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/purelanren/skills/multi-city-flight-optimizer)
- [FlyAI command reference](artifact/reference/flyai-commands.md)
- [Output format templates](artifact/reference/output-templates.md)
- [HTML visualization template](artifact/reference/html-template.md)
- [Tool usage guide](artifact/reference/tools-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown responses with shell command examples and optional generated HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use remembered travel preferences and may create shareable HTML comparison files when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
