## Description: <br>
YouTube SERP Scout for agents. Search top-ranking videos, channels, and trends for content research and competitor tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIsaDocs](https://clawhub.ai/user/AIsaDocs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agents use this skill to research YouTube search results, discover top-ranking videos and channels, monitor competitors, and compare regional or language-specific results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends YouTube search terms to AIsa's external API using a declared AISA_API_KEY. <br>
Mitigation: Use a dedicated API key where possible, monitor usage and costs, and avoid submitting secrets, personal data, customer names, or confidential research terms unless policy allows sharing them with AIsa. <br>
Risk: The skill depends on AIsa as the external YouTube search provider. <br>
Mitigation: Install and use it only if the external provider is acceptable for the intended workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/AIsaDocs/openclaw-aisa-youtube-search-tracking) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>
- [AIsa API reference](https://aisa.mintlify.app/api-reference/introduction) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash examples, Python client usage, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and sends YouTube search queries to AIsa's external API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
