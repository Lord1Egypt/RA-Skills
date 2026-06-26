## Description: <br>
Fetches Google Trends data including daily trending topics, real-time trends, interest by region, related topics, related queries, and autocomplete suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terryds](https://clawhub.ai/user/terryds) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to retrieve Google Trends data for trending searches, keyword popularity, regional interest, related topics, related queries, and autocomplete suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trend keywords and region or time parameters are sent to Google Trends, and the skill relies on unofficial Google Trends endpoints that may rate-limit or change. <br>
Mitigation: Avoid sending sensitive query terms, review outputs before relying on them, and retry later or update the skill if Google rate-limits requests or changes endpoint behavior. <br>


## Reference(s): <br>
- [Google Trends Skill Command Reference](reference.md) <br>
- [trends-js](https://github.com/Shaivpidadi/trends-js) <br>
- [ClawHub Skill Page](https://clawhub.ai/terryds/google-trends-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [JSON from the bundled command-line script, typically summarized by the agent as markdown tables, lists, or prose.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries may send trend keywords, region codes, language codes, and time ranges to Google Trends.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
