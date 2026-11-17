## Description:

Search LovTrip travel guides, destinations, and itinerary ideas without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizhijun](https://clawhub.ai/user/lizhijun)

### License/Terms of Use:


## Use Case:

External users and travel-planning assistants use this skill to search travel guides, browse destinations, and retrieve itinerary templates from LovTrip using either public HTTPS API calls or the LovTrip CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the unpinned LovTrip CLI through npx can execute changing third-party code locally.

Mitigation: Prefer the documented curl HTTPS API examples; if CLI use is necessary, pin and review the lovtrip package version and run it in a sandbox with minimal file and credential access.

Risk: Travel search queries may include sensitive personal itinerary details.

Mitigation: Avoid sending sensitive personal, credential, or private trip information in LovTrip search queries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lizhijun/skills/lovtrip-content)
- [LovTrip](https://lovtrip.app)
- [LovTrip Developer Documentation](https://lovtrip.app/developer)
- [LovTrip Planner](https://lovtrip.app/planner)
- [LovTrip Guides](https://lovtrip.app/guides)
- [Search Guides Examples](examples/search-guides.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return CLI-formatted text or JSON from LovTrip public API calls.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
