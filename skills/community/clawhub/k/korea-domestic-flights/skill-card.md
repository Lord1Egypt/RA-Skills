## Description: <br>
Searches, compares, and monitors Korean domestic flights with Playwright-backed workflows for route, date-range, multi-destination, and price-alert tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twbeatles](https://clawhub.ai/user/twbeatles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers, travel operators, and agents use this skill to search Korean domestic one-way and round-trip fares, compare dates and destinations, generate fare briefings, and manage target-price watch rules. <br>

### Deployment Geography for Use: <br>
South Korea <br>

## Known Risks and Mitigations: <br>
Risk: Searches execute code from an unpinned local tmp/Scraping-flight-information scraper clone outside the reviewed package. <br>
Mitigation: Use only after verifying the local scraper clone and its dependencies; pin or review that dependency before running live searches. <br>
Risk: Price-alert rules can store routes, travel dates, target prices, notes, and message templates in a local JSON file. <br>
Mitigation: Create recurring checks intentionally, protect the rule file as user travel data, and remove old rules when they are no longer needed. <br>
Risk: Live fare results depend on browser automation and external flight-search site behavior. <br>
Mitigation: Treat fares as point-in-time results, use the fixture and dry-run checks before relying on automation, and confirm prices before purchase. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twbeatles/korea-domestic-flights) <br>
- [README](README.md) <br>
- [Domestic Airport Codes](references/domestic-airports.md) <br>
- [Price Alert JSON Format](references/price-alerts-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Human-readable Korean briefings, JSON search results, alert-rule JSON, and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Price alert checks can write local watch-rule state and print alert messages to stdout.] <br>

## Skill Version(s): <br>
0.6.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
