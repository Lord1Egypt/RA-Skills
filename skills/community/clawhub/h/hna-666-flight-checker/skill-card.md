## Description: <br>
Checks Hainan Airlines 666Plus round-trip benefit flight availability from Beijing across configured destinations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aywd2026](https://clawhub.ai/user/aywd2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers or travel-planning agents use this skill to check whether Hainan Airlines 666Plus benefit round trips are available between Beijing and configured destinations for supplied outbound and return dates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local browser automation and repeatedly queries Hainan Airlines availability pages. <br>
Mitigation: Install only in a trusted local environment, verify the Playwright runtime path, and ensure the user has permission to automate the site. <br>
Risk: Flight availability can change after the skill reports a matching route. <br>
Mitigation: Confirm availability directly with Hainan Airlines before relying on results for travel decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aywd2026/hna-666-flight-checker) <br>
- [Hainan Airlines 666Plus availability query](https://m.hnair.com/hnams/plusMember/ableAirlineQuery) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text results with command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires outbound and return dates; reports eligible round-trip destinations from the configured destination list.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
