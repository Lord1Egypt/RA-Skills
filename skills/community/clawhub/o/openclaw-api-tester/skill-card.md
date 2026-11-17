## Description:

Test API endpoints and document responses. Define tests in plain English, run them, get formatted results. Agent-driven Postman alternative.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and API testers use this skill to define endpoint tests in plain English, execute them against configured environments, and produce documented API test results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send arbitrary API requests from the user's environment.

Mitigation: Run tests against sandbox or staging endpoints and review target URLs, headers, and methods before execution.

Risk: State-changing requests can alter or delete data when run with production access.

Mitigation: Avoid production credentials unless necessary and require review before running POST, PUT, PATCH, or DELETE tests.

Risk: Generated reports or stored response bodies may contain sensitive API data.

Mitigation: Redact secrets and sensitive response fields before sharing reports, and keep local outputs in an appropriate secured location.

Risk: Tests supplied by untrusted files or prompts can target unintended hosts or include unsafe headers.

Mitigation: Inspect test definitions, base URLs, request bodies, and headers before allowing the agent to run them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/openclaw-api-tester)
- [Publisher profile](https://clawhub.ai/user/theshadowrose)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, JSON result objects, generated API documentation, and optional HTML, JSON, or Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include HTTP status codes, response times, pass/fail summaries, response bodies, and generated API documentation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
