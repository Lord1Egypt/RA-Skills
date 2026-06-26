## Description: <br>
Input a news URL to efficiently extract the body, title, author, and date using a remote API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fonilye](https://clawhub.ai/user/fonilye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to extract a title, author, publication date, and body text from public news URLs through a remote extraction API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the API key and user-supplied news URL to a configured backend while HTTPS certificate validation is disabled. <br>
Mitigation: Use only news URLs and an EasyAlpha API key that are acceptable to send to the backend, avoid private or credential-bearing URLs, and prefer a release that restores normal HTTPS certificate validation before using real credentials. <br>


## Reference(s): <br>
- [OpenClaw](https://openclaw.ai) <br>
- [EasyAlpha API key portal](https://easyalpha.duckdns.org) <br>
- [Default news extraction API endpoint](https://easyalpha.duckdns.org/api/v1/extract) <br>
- [ClawHub skill page](https://clawhub.ai/fonilye/news-content) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, API Calls, Configuration] <br>
**Output Format:** [JSON from the extractor script, typically presented by the agent as text or Markdown fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, EASYALPHA_API_KEY, and optionally NEWS_EXTRACTOR_SERVER_URL.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
