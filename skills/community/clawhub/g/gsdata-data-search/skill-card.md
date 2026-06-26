## Description: <br>
Parses Chinese natural-language ES search requests, calls a local social-media/news search API, and returns matching results as Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urhd528](https://clawhub.ai/user/urhd528) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to convert Chinese natural-language search requests into ES API parameters and retrieve social-media or news records by keyword, platform, time range, and sentiment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores app_key credentials in a local config.json file and can display that configuration. <br>
Mitigation: Use a limited-purpose app_key, avoid sharing --show-config output, and clear config.json when finished. <br>
Risk: Search terms and app-key-based headers are sent to the configured local ES search service during normal API mode. <br>
Mitigation: Install only when that service is expected and approved for the data being searched. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/urhd528/gsdata-data-search) <br>
- [Publisher profile](https://clawhub.ai/user/urhd528) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown search-result table or JSON search parameters, with plain-text error guidance when configuration or API calls fail] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads or writes local config.json for app_key credentials; default API mode sends search terms and app-key-derived headers to a local ES search service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
