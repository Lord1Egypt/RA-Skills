## Description: <br>
Search for products on Naver Shopping. Use when the user wants to find product prices, links, or compare items in the Korean market. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twbeatles](https://clawhub.ai/user/twbeatles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Naver Shopping for Korean-market product listings, prices, and links from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product search terms are sent to Naver and the script uses Naver Shopping API credentials. <br>
Mitigation: Use dedicated Naver credentials, store them only in the documented skill-specific locations, and avoid submitting sensitive search terms. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/twbeatles/naver-shopping-twbeatles) <br>
- [Naver Shopping Search API endpoint](https://openapi.naver.com/v1/search/shop.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search results and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Naver Shopping API credentials and accepts query, display count, and sort order.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
