## Description: <br>
Hunt helps an agent find, vet, track, and manage online hackathon opportunities with map tracking and reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lloyd-c137](https://clawhub.ai/user/lloyd-c137) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Hunt to scout free online hackathons, compare prize and eligibility details, save selected events to a map.md tracker, and receive reminders before events start. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Accidental activation could start web browsing or tracker actions unexpectedly. <br>
Mitigation: Use explicit commands such as "find hackathons", "show map", or "add 1 to map" before invoking the workflow. <br>
Risk: Tracker reset commands can archive the map and remove reminder jobs. <br>
Mitigation: Confirm the user's intent before running "clear map" or "reset map", and preserve the generated archive. <br>
Risk: Separate packaged skill or CLI files may contain behavior not represented by the submitted markdown artifact. <br>
Mitigation: Review any packaged skill or CLI files before installation or deployment. <br>
Risk: Hackathon listings can become stale or contain unclear prize, cost, or eligibility details. <br>
Mitigation: Verify event pages before presenting recommendations and mark uncertain prize details as needing confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lloyd-c137/hunt) <br>
- [Publisher profile](https://clawhub.ai/user/lloyd-c137) <br>
- [Repository metadata URL](https://github.com/lloyd-c137/hunt-skill) <br>
- [Map format reference](references/map-format.md) <br>
- [MLH events](https://events.mlh.io/) <br>
- [Devpost hackathons](https://devpost.com/hackathons) <br>
- [Devfolio hackathons](https://devfolio.co/hackathons) <br>
- [lablab.ai hackathons](https://lablab.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Telegram-friendly Markdown or plain text, map.md tracker entries, and reminder scheduling requests.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Avoids Markdown tables for Telegram; includes plain links and prize lines for listed hackathons.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
