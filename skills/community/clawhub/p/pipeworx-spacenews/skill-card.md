## Description: <br>
Provides the latest spaceflight news articles and blog posts with keyword search via the Spaceflight News API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve recent spaceflight articles, search space-news coverage by keyword, and collect current blog posts with source URLs and publication metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Space-news search terms are sent to the disclosed Pipeworx gateway. <br>
Mitigation: Do not include secrets, private material, or sensitive internal topics in searches. <br>
Risk: Returned articles and blog posts come from upstream news sources and may be incomplete, delayed, or inaccurate. <br>
Mitigation: Check important facts against the linked source outlet before relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/brucegutman/pipeworx-spacenews) <br>
- [Publisher profile](https://clawhub.ai/user/brucegutman) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Structured article and blog results with title, summary, URL, image, source outlet, and publication timestamp.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports latest-article, keyword-search, and latest-blog retrieval; results depend on the disclosed remote gateway and upstream news sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
