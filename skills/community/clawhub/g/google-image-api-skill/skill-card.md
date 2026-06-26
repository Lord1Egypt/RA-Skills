## Description: <br>
This skill helps users automatically extract structured image data from Google Images via the BrowserAct API for image sourcing, visual research, competitor monitoring, localized trend tracking, and metadata collection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccmagia2-gif](https://clawhub.ai/user/ccmagia2-gif) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and research teams use this skill to run keyword-based Google Images searches through BrowserAct and receive structured result metadata such as titles, source sites, thumbnails, click-through links, product indicators, and result indexes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image-search keywords, locale settings, and returned result metadata are sent to BrowserAct and Google Images through the user's BrowserAct account. <br>
Mitigation: Avoid sensitive or confidential search terms and use a dedicated or limited BrowserAct API key where possible. <br>
Risk: The skill depends on a valid BrowserAct API key and external service availability. <br>
Mitigation: Confirm BROWSERACT_API_KEY is configured before running and stop rather than retrying when authorization is invalid. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ccmagia2-gif/google-image-api-skill) <br>
- [BrowserAct API Key Console](https://www.browseract.com/reception/integrations) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text logs and structured Google Images result metadata returned by the BrowserAct API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BROWSERACT_API_KEY and accepts keyword, country, language, scroll count, and result limit inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
