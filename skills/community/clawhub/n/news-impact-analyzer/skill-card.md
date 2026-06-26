## Description: <br>
Input news text and use an LLM to analyze its impact on stock market sectors and concepts (bullish/bearish/neutral) along with the underlying logic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fonilye](https://clawhub.ai/user/fonilye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents, developers, and investment researchers use this skill to submit news text and receive a concise market-impact analysis across sectors and concepts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted news text and the API key are sent to the EasyAlpha backend. <br>
Mitigation: Use the skill only with a trusted backend and avoid submitting confidential, proprietary, unpublished, or regulated information unless separate handling and retention assurances are in place. <br>
Risk: HTTPS certificate verification is disabled by default, and users can configure a plain HTTP or untrusted backend URL. <br>
Mitigation: Set ALLOW_INSECURE_SSL=false before use and avoid plain HTTP or untrusted NEWS_EXTRACTOR_SERVER_URL values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fonilye/news-impact-analyzer) <br>
- [EasyAlpha service registration and default backend](https://easyalpha.duckdns.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Formatted text or Markdown; JSON responses are rendered as a summary plus sector/concept impact lines.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and EASYALPHA_API_KEY; sends submitted news text to a remote EasyAlpha analysis API.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
