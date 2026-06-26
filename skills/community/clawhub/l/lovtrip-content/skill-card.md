## Description: <br>
Travel Content Browser for searching LovTrip travel guides, destinations, and itineraries without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lizhijun](https://clawhub.ai/user/lizhijun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search LovTrip travel content, browse destinations, and retrieve itinerary ideas through the LovTrip CLI or public API examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel searches, destination interests, and itinerary queries are sent to lovtrip.app. <br>
Mitigation: Avoid sending sensitive personal travel details unless the user is comfortable sharing them with LovTrip. <br>
Risk: The optional CLI examples run an external npm package through npx lovtrip@latest. <br>
Mitigation: Prefer the curl examples, or pin and review the npm CLI version before running it in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lizhijun/lovtrip-content) <br>
- [LovTrip](https://lovtrip.app) <br>
- [LovTrip developer documentation](https://lovtrip.app/developer) <br>
- [LovTrip travel guides](https://lovtrip.app/guides) <br>
- [Search guide examples](examples/search-guides.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use npx lovtrip or curl examples to fetch LovTrip search, guide, destination, and itinerary content.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
