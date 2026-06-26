## Description: <br>
Media Search helps agents search a media big-data API for news, background material, policy updates, industry data, and source coverage by keyword, time range, source, and data type. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liushilong-dodo](https://clawhub.ai/user/liushilong-dodo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Journalists, researchers, content teams, and agents use this skill to search configured media sources for coverage, context, source material, and recent developments. It supports filtered searches and can return results to the console or save them for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports unsafe API credential handling, including token or header logging and a local token cache. <br>
Mitigation: Review the skill before sensitive use, remove token and header logging, and protect or avoid local token caching. <br>
Risk: The security review reports disabled HTTPS certificate verification. <br>
Mitigation: Enable HTTPS certificate verification before using the skill in sensitive or production environments. <br>
Risk: Search terms and filters are sent to an external media API. <br>
Mitigation: Avoid sensitive queries unless the API provider and local machine are trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liushilong-dodo/media-search) <br>
- [Media Big Data API endpoint](https://mbdapi.fzdzyun.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Formatted console text, Markdown result files, and JSON result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NEWS_BIGDATA_API_KEY and NEWS_BIGDATA_API_SECRET for API access; results may be saved under a sources directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
