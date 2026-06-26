## Description: <br>
Analyze Web Page workflows with JustOneAPI, including HTML content, rendered HTML content, and Markdown content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justoneapi](https://clawhub.ai/user/justoneapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch web page HTML, rendered HTML, or Markdown content from JustOneAPI for API-backed page analysis. It is suited to URL-scoped retrieval tasks where the user can provide the target page URL and an API token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitting private, internal-only, access-controlled, or secret-bearing URLs may disclose sensitive page locations or fetched content to JustOneAPI. <br>
Mitigation: Use only URLs whose submission and retrieved content are acceptable to share with JustOneAPI. <br>
Risk: The JustOneAPI token could be exposed through chat messages, screenshots, command logs, or error output. <br>
Mitigation: Pass the token through JUST_ONE_API_TOKEN or the helper token argument, keep it out of shared logs, and rotate it if exposure is suspected. <br>
Risk: Fetched web content can be incomplete, stale, or affected by the target site's rendering and access behavior. <br>
Mitigation: Treat API output as retrieval evidence for the requested URL and verify critical findings against the source page when accuracy matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justoneapi/justoneapi-web) <br>
- [JustOneAPI Homepage](https://api.justoneapi.com) <br>
- [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_web&utm_content=project_link) <br>
- [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_web&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a URL parameter and JUST_ONE_API_TOKEN for authenticated JustOneAPI requests.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
