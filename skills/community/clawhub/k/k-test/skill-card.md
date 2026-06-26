## Description: <br>
Search X (Twitter) posts using the xAI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dtkien1802](https://clawhub.ai/user/dtkien1802) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to search X/Twitter posts in real time through the xAI Grok API, with optional filters for handles, exclusions, date ranges, images, and video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses XAI_API_KEY as a secret credential. <br>
Mitigation: Keep XAI_API_KEY in environment or approved local configuration only, avoid committing or sharing it, and rotate it if exposed. <br>
Risk: Search queries are sent to xAI for processing. <br>
Mitigation: Avoid submitting sensitive or confidential query text unless that use is approved for the xAI API. <br>


## Reference(s): <br>
- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search) <br>
- [xAI Console](https://console.x.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON search results with text, citations, links, status, query, search count, and token usage; skill guidance is Markdown with bash examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and XAI_API_KEY; supports handle filters, excluded handles, date ranges, image understanding, and video understanding.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
