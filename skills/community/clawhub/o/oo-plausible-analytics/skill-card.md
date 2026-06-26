## Description: <br>
This skill operates Plausible Analytics through an OOMOL-connected account to query site analytics and record pageview or custom events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to inspect Plausible site traffic, breakdowns, timeseries data, and real-time analytics. It can also help record tracking events after the user confirms the target site, event name, payload, and expected analytics impact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The record_event action can write Plausible Analytics events, and the security evidence says this write action is under-labeled. <br>
Mitigation: Before running record_event, confirm the exact site, event name, payload, and expected analytics impact with the user. <br>
Risk: The skill requires an OOMOL-connected Plausible Analytics account. <br>
Mitigation: Install and use it only when the user intends to operate Plausible Analytics through OOMOL-connected credentials. <br>


## Reference(s): <br>
- [ClawHub Plausible Analytics Skill](https://clawhub.ai/oomol/oo-plausible-analytics) <br>
- [Plausible Analytics](https://plausible.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the oo CLI to return connector responses as JSON with data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
