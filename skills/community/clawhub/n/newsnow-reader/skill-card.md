## Description: <br>
优雅地阅读实时热门新闻。支持微博、知乎、百度、抖音、华尔街见闻、今日头条、澎湃新闻等8个主流平台。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Castieler](https://clawhub.ai/user/Castieler) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch current hot-news lists from supported third-party news and social platforms, then view the results as JSON, compact text, Markdown, or an elegant terminal summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to multiple third-party news and social-media domains. <br>
Mitigation: Review the disclosed domains before running it from a sensitive network and restrict egress if needed. <br>
Risk: The implementation includes a Jin10 source in code that is not fully documented in the visible source table. <br>
Mitigation: Review the Jin10 endpoint and behavior before enabling or relying on that source. <br>
Risk: Third-party platform APIs, cookies, and page structures may change or rate-limit requests. <br>
Mitigation: Treat failed or empty results as expected operational failures and verify important news against the original linked source. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Castieler/newsnow-reader) <br>
- [newsnow implementation reference](https://github.com/ourongxing/newsnow) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON arrays and Markdown or terminal-formatted text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are limited by the requested source and item count, defaulting to a single hot-news list.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
