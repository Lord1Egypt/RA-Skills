## Description: <br>
YouTube SERP Scout for agents. Search top-ranking videos, channels, and trends for content research and competitor tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaimengphp](https://clawhub.ai/user/chaimengphp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content researchers, and marketing teams use this skill to query YouTube search results through AIsa for rank discovery, content research, competitor tracking, trend discovery, keyword research, and regional audience research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, competitor names, locale filters, and API authorization are sent to api.aisa.one. <br>
Mitigation: Use only approved queries and avoid confidential internal topics or secrets unless external disclosure to AIsa is approved by the organization. <br>
Risk: The skill depends on an AISA_API_KEY and external network access to AIsa. <br>
Mitigation: Store the API key in the environment, rotate it according to organizational policy, and restrict use to environments allowed to call api.aisa.one. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chaimengphp/openclaw-aisa-youtube-search) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash, Python, and JSON examples; the bundled client prints JSON responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, curl, and AISA_API_KEY; sends YouTube search requests to api.aisa.one.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
