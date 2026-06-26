## Description: <br>
Fetches trending news and hot topics from 66 sources across 44 platforms, returning titles, URLs, and metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeguooooo](https://clawhub.ai/user/leeguooooo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to list available news sources, fetch trending items from selected platforms, and request structured JSON for downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs the newsnow npm CLI directly or through npx. <br>
Mitigation: Install or execute it only when the npm package source is trusted, and review commands before running them. <br>
Risk: The Product Hunt source can require PRODUCTHUNT_API_TOKEN. <br>
Mitigation: Set the token only when Product Hunt results are needed, and use a minimally scoped token where possible. <br>
Risk: Some sources may fail because of Cloudflare blocking or regional network availability. <br>
Mitigation: Treat 403 responses or empty results as source availability issues and choose an alternate source when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leeguooooo/leeguooooo-newsnow) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI results may be readable text or JSON news items.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output includes item identifiers, titles, optional URLs, publication dates, and extra metadata when provided by the source.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
