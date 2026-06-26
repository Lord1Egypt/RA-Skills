## Description: <br>
Real-time world news briefings with AI-clustered events, topic classification, and geographic filtering. No API key needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pranciskus](https://clawhub.ai/user/pranciskus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, employees, and developers use this skill to fetch current news events and format concise briefings by topic, geography, time window, and event importance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: News-related queries and filters are sent to the NewsMCP service. <br>
Mitigation: For sensitive or ambiguous conversations, ask before making a live news request. <br>
Risk: Live news results depend on NewsMCP service availability, source coverage, and AI-generated summaries. <br>
Mitigation: Present source links with briefings and avoid treating summaries as the only source of record. <br>


## Reference(s): <br>
- [NewsMCP homepage](https://newsmcp.io) <br>
- [NewsMCP API base](https://newsmcp.io/v1) <br>
- [ClawHub skill page](https://clawhub.ai/pranciskus/newsmcp-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown briefings with inline source links and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live NewsMCP API responses; requires curl for example commands; no API key required.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
