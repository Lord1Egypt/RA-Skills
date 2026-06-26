## Description: <br>
Search for golf tee times and deals near any location, compare prices across platforms, and provide discount tips when asked about golf, tee times, courses, or booking a round. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tag-assistant](https://clawhub.ai/user/tag-assistant) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to search GolfNow tee times, compare course availability and prices, identify discounts, and prepare booking options. The skill can also guide a booking workflow that requires explicit user approval before completing a paid reservation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use stored GolfNow credentials and saved payment details to complete paid tee-time reservations. <br>
Mitigation: Install only when booking authority is intended; require a checkout screenshot and explicit user approval before any reservation is submitted. <br>
Risk: The skill depends on GolfNow pages and API behavior that may change and can affect availability, pricing, rewards, or checkout steps. <br>
Mitigation: Verify final course, time, player count, price, fees, rewards, and payment details on the checkout page before approving a booking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tag-assistant/golf-tee-times) <br>
- [GolfNow](https://www.golfnow.com) <br>
- [GolfNow tee-time results API endpoint](https://www.golfnow.com/api/tee-times/tee-time-results) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tee-time summaries, plain text or JSON search results, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and python3; may use external GolfNow endpoints and local credential setup for booking flows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
