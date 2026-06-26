## Description: <br>
Power Search is a self-hosted research tool that combines Brave Search API with Browserless content fetching for web search, optional full-page extraction, and HTML parsing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[churchtg7](https://clawhub.ai/user/churchtg7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and external users use Power Search to run web searches through Brave and optionally fetch and parse page content through Browserless from a CLI or OpenClaw Telegram route. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Brave Search. <br>
Mitigation: Use a dedicated Brave API key and avoid submitting sensitive queries unless that disclosure is acceptable. <br>
Risk: Fetch mode sends result URLs and retrieved page content through the configured Browserless service. <br>
Mitigation: Bind or firewall Browserless to trusted hosts and avoid sensitive or internal-only targets. <br>
Risk: Telegram usage can expose search results or fetched content to shared chats. <br>
Mitigation: Use private or trusted channels for sensitive searches and review chat membership before enabling the route. <br>
Risk: A persistent Browserless container may keep a network-fetching service available longer than intended. <br>
Mitigation: Stop the container when it is not needed and restrict network access to trusted clients. <br>


## Reference(s): <br>
- [Power Search ClawHub Page](https://clawhub.ai/churchtg7/power-search) <br>
- [Power Search Skill Documentation](artifact/SKILL.md) <br>
- [Power Search README](artifact/README.md) <br>
- [Security and Transparency Report](artifact/SECURITY.md) <br>
- [OpenClaw Manifest](artifact/openclaw.json) <br>
- [Brave Search API](https://api.search.brave.com/res/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; runtime search output is plain text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional fetch mode retrieves page content previews through the configured Browserless service.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release metadata; artifact files report 2.0.0 and SECURITY.md reports 2.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
