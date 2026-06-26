## Description: <br>
Complete AI brand-visibility toolkit via MentionsAPI.com for checking brand mentions, ranks, and citations across major AI answer surfaces, discovering queries to track, comparing brands or queries, and monitoring changes over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nikhonit](https://clawhub.ai/user/nikhonit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, SEO/GEO, and competitive-intelligence teams use this skill to measure whether specific brands appear in AI-generated answers, discover visibility queries, compare competitors, and set up monitored change alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MentionsAPI calls require a live API key and may consume paid credits. <br>
Mitigation: Use the skill only for explicit AI-visibility requests, confirm the brand and query when intent is ambiguous, and monitor wallet balance before repeated or scheduled calls. <br>
Risk: watch_brand sends brand-visibility data to a configured webhook and relies on a shared secret. <br>
Mitigation: Use an HTTPS endpoint you control, verify HMAC signatures on every delivery, reject unsigned or replayed requests, and store or rotate webhook_secret like a password. <br>


## Reference(s): <br>
- [MentionsAPI homepage](https://mentionsapi.com) <br>
- [MentionsAPI check API documentation](https://mentionsapi.com/docs/api/check) <br>
- [MentionsAPI OpenAPI specification](https://mentionsapi.com/openapi.json) <br>
- [MentionsAPI recipes](https://mentionsapi.com/docs/recipes) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, guidance] <br>
**Output Format:** [JSON-like Python dictionaries with concise text guidance for setup and error handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MENTIONSAPI_KEY; usage can consume MentionsAPI credits, and watch_brand requires a user-controlled HTTPS webhook with a securely handled secret.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
