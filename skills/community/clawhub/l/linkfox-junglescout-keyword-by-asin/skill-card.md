## Description: <br>
Queries Jungle Scout keyword data for up to 10 Amazon ASINs, returning keyword search volume, competition, PPC bid, ranking, and relevancy metrics across supported marketplaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon sellers, marketplace analysts, and e-commerce operators use this skill to discover and compare keywords associated with competitor or target ASINs. It supports keyword expansion, traffic-source analysis, and PPC bid research using LinkFox-authenticated Jungle Scout data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox API key and sends ASIN research and query parameters to LinkFox services. <br>
Mitigation: Install only when that data sharing is acceptable, keep LINKFOXAGENT_API_KEY out of prompts and logs, and avoid adding confidential business context to requests. <br>
Risk: The release security summary reports automatic feedback submission to a separate LinkFox endpoint without clear user approval. <br>
Mitigation: Review feedback behavior before installation and disable or constrain feedback calls where user consent or organizational policy requires it. <br>


## Reference(s): <br>
- [Jungle Scout ASIN keyword API reference](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-junglescout-keyword-by-asin) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries and tables derived from JSON API responses, with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and accepts marketplace, ASIN list, result count, sorting, variant inclusion, and keyword metric filters.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
