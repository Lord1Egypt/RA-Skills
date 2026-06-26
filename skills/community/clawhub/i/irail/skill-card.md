## Description: <br>
Query Belgian railway (NMBS/SNCB) schedules via the irail CLI for departures, route connections, train composition, and service disruption information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dedene](https://clawhub.ai/user/dedene) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to answer Belgian rail travel questions by running the irail CLI against public NMBS/SNCB data. It supports live station boards, connections, stations, vehicles, train composition, and disruptions without requiring authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on installing and trusting a third-party irail CLI package through Homebrew or Go. <br>
Mitigation: Install only after reviewing the referenced package source and use normal caution for third-party command-line tools. <br>
Risk: Repeated scripted calls can place unnecessary load on the public iRail API. <br>
Mitigation: Add delays or reasonable rate limits when using the CLI in loops. <br>
Risk: Rail schedule and disruption data is time-sensitive and can change after retrieval. <br>
Mitigation: Refresh liveboard, connection, or disturbance queries before presenting time-critical travel guidance. <br>


## Reference(s): <br>
- [ClawHub Irail skill page](https://clawhub.ai/dedene/irail) <br>
- [irail-cli homepage](https://github.com/dedene/irail-cli) <br>
- [iRail API](https://api.irail.be/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash commands, JSON parsing examples, and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include irail CLI commands with --json, jq filters, language flags, time/date options, and installation guidance; no credentials are required.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter metadata reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
