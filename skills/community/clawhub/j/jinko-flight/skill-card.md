## Description: <br>
Guide for using the Jinko CLI (@gojinko/cli), a terminal tool for searching flights, discovering destinations, managing trips, and booking travel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevinjinko](https://clawhub.ai/user/kevinjinko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate the Jinko CLI for flight search, destination discovery, trip setup, and travel checkout workflows from a terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports travel booking flows that can collect traveler identity and contact details. <br>
Mitigation: Use it only when the user is comfortable sharing traveler and contact information with the booking provider. <br>
Risk: Booking commands or payment flows can affect real travel purchases. <br>
Mitigation: Require the agent to show the exact trip, traveler fields, price, and checkout destination before running booking commands or opening payment flows. <br>
Risk: Cached flight results may be stale before checkout. <br>
Mitigation: Confirm live pricing with the CLI price-check workflow before creating a trip or booking. <br>


## Reference(s): <br>
- [Jinko ClawHub skill page](https://clawhub.ai/kevinjinko/jinko-flight) <br>
- [kevinjinko publisher profile](https://clawhub.ai/user/kevinjinko) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include terminal commands that search flights, manage trips, set traveler/contact details, and open booking checkout flows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
