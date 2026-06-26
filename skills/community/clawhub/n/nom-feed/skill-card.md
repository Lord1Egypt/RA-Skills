## Description: <br>
Fetch recent GitHub activity from the Nom feed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lws803](https://clawhub.ai/user/lws803) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and repository maintainers use this skill to look up recent GitHub activity for a repository or global feed, filter by event type, organization, search text, date range, and result limit, and receive a readable activity summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, repository names, and filter values are sent to the disclosed Nom service. <br>
Mitigation: Use the skill for public GitHub activity searches and avoid sensitive private search terms or repository details. <br>
Risk: Unquoted or unencoded user input could produce malformed curl requests. <br>
Mitigation: Quote and URL-encode user-provided arguments when forming requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lws803/nom-feed) <br>
- [Nom feed service](https://beta.nomit.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries, with optional RSS XML when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl requests to the Nom service; default result limit is 20 and maximum result limit is 100.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
