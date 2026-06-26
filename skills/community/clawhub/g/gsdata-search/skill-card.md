## Description: <br>
Searches the projects-databus.gsdata.cn API with a project ID, API signature, keywords, date range, and optional result limit, returning filtered news result data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urhd528](https://clawhub.ai/user/urhd528) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to query GS Data search results and receive filtered news items for downstream analysis or reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the API signature and search terms over unencrypted HTTP. <br>
Mitigation: Use only trusted GS Data endpoints, avoid sensitive keywords, prefer an HTTPS-supported version, and rotate scoped signatures if exposure is possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/urhd528/gsdata-search) <br>
- [Publisher profile](https://clawhub.ai/user/urhd528) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text] <br>
**Output Format:** [Python list of dictionaries or command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Filters each result to news_title, news_uuid, media_name, news_posttime, news_emotion, news_url, and news_digest.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
