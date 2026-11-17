## Description:

Explains HTTP status codes in plain language and suggests safe next steps for clients and operators debugging APIs, browsers, or reverse proxies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmahmadcs](https://clawhub.ai/user/hmahmadcs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to interpret HTTP responses, identify who should act, and choose practical debugging steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted HTTP responses may expose credentials or other secrets.

Mitigation: Do not share API keys, cookies, or Authorization headers; redact sensitive fields and rotate any exposed secrets.

Risk: A status code alone may not reveal the actual cause of a failure.

Mitigation: Treat suggested causes as hypotheses and verify them against available headers, logs, and upstream health checks.

## Reference(s):

- [MDN HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [ClawHub skill listing](https://clawhub.ai/hmahmadcs/skills/http-status-explainer)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Short sections covering meaning, likely causes, responsible party, and next checks; optional incident-channel summary.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
