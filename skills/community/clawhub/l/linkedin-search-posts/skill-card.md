## Description: <br>
Search LinkedIn posts by keywords using the Apify actor harvestapi/linkedin-post-search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Godefroy](https://clawhub.ai/user/Godefroy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and analysts use this skill to search and retrieve LinkedIn posts that match keywords, author or company filters, date limits, and sort preferences through Apify. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LinkedIn search terms, filters, and retrieved post data are sent through Apify. <br>
Mitigation: Use the skill only when that data flow is acceptable, and review Apify and LinkedIn compliance obligations before broad or sensitive collection. <br>
Risk: Apify tokens may appear in tokenized API URLs, logs, or command history. <br>
Mitigation: Use a dedicated or scoped APIFY_API_TOKEN where possible and avoid sharing logs, transcripts, or shell history that contain token URLs. <br>
Risk: Scraping reactions and comments can increase collected data volume and cost. <br>
Mitigation: Set explicit maxPosts, maxComments, and maxReactions limits before running searches. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Godefroy/linkedin-search-posts) <br>
- [Publisher profile](https://clawhub.ai/user/Godefroy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON request/response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Apify API invocation guidance and describes JSON result fields for LinkedIn posts, reactions, and comments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
