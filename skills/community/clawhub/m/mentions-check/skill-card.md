## Description: <br>
Checks whether a brand is mentioned, ranked, and cited across AI search surfaces through MentionsAPI.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nikhonit](https://clawhub.ai/user/nikhonit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, SEO, and growth teams use this skill to measure whether a named brand appears, how it ranks, and which sources are cited for a specific AI-search question across supported providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports a suspicious review helper that can launch nested review with sandbox and approval bypass authority. <br>
Mitigation: Install only if the publisher is trusted, and use --no-yolo or AUTOREVIEW_YOLO=0 before running autoreview so nested review does not bypass sandbox and approval protections by default. <br>
Risk: The skill requires a MentionsAPI key and makes paid API calls, so ambiguous or repeated checks can spend credits and send brand and query data to MentionsAPI. <br>
Mitigation: Run it only after confirming the brand, query, mode, and runs count; store MENTIONSAPI_KEY only in the environment, start with the lowest-cost mode, and rotate the key if it is exposed. <br>


## Reference(s): <br>
- [MentionsAPI homepage](https://mentionsapi.com) <br>
- [ClawHub skill listing](https://clawhub.ai/nikhonit/mentions-check) <br>
- [MentionsAPI check endpoint reference](https://mentionsapi.com/docs/api/check) <br>
- [MentionsAPI OpenAPI spec](https://mentionsapi.com/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON-compatible Python dict with per-provider mention, rank, context, citation, cost, balance, or error details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MENTIONSAPI_KEY. API calls may consume paid credits, and mode or runs settings can change cost.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
