## Description: <br>
Scrape structured news data from Google News automatically for topic news searches, industry trend tracking, and PR monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[phheng](https://clawhub.ai/user/phheng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to collect structured Google News results for topics, industry trends, company monitoring, and PR monitoring through BrowserAct. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask users to provide a BrowserAct API key in chat. <br>
Mitigation: Configure BROWSERACT_API_KEY outside chat and stop if an unexpected prompt requests the credential. <br>
Risk: Google News search terms are sent to BrowserAct. <br>
Mitigation: Avoid sensitive queries and install only when sharing news search terms with BrowserAct is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/phheng/google-news-api) <br>
- [BrowserAct integration console](https://www.browseract.com/reception/integrations) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and structured news result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BROWSERACT_API_KEY and returns headline, source, news link, published time, and author fields when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
