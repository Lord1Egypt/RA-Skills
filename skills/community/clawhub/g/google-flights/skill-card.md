## Description: <br>
Search Google Flights for prices, availability, deals, flexible dates, filtered options, connection quality, and price-tracking alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kris-hansen](https://clawhub.ai/user/kris-hansen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search and compare flight options, evaluate flexible travel dates and filters, and monitor route prices against alert thresholds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight searches are handled through the fast-flights/Google Flights path. <br>
Mitigation: Install only if that routing is acceptable for the user's flight-search workflow. <br>
Risk: Price tracking and route watching save route, date, and price history locally under ~/clawd/memory. <br>
Mitigation: Remove tracked routes and delete the local memory files when alerts or history are no longer needed. <br>
Risk: The cron example can enable recurring background price checks. <br>
Mitigation: Enable scheduled checks only when recurring monitoring is desired, and review or remove the cron entry when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Google Flights skill page](https://clawhub.ai/kris-hansen/google-flights) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON flight search and tracking results, with shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store local route, tracking, and price-history files under ~/clawd/memory when tracking features are used.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
