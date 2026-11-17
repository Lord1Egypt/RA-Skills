## Description:

Automates quick, no-credential public website checks such as summaries, keyword checks, and simple page facts through the local OpenClaw Automation Kit query path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcosathanasoulis](https://clawhub.ai/user/marcosathanasoulis)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run public webpage automation checks, extract page facts, count keyword mentions, and return concise highlights without collecting credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill states that it is for public websites only, but evidence.security reports that it does not enforce that network boundary.

Mitigation: Run it only in environments where unrestricted outbound requests are acceptable, or add URL and redirect validation that permits only public http/https destinations and blocks localhost, private IP ranges, link-local metadata endpoints, and unsafe redirects.

Risk: Using the skill for login-required or credentialed workflows would exceed the artifact's documented safety boundary.

Mitigation: Use it only for no-credential public page checks and route login-required tasks to a separate reviewed flow.

## Reference(s):

- [Openclaw Web Automation on ClawHub](https://clawhub.ai/marcosathanasoulis/skills/openclaw-web-automation)
- [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/schema)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON results with concise Markdown-facing summary guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes success status, script identifiers, result object, parsed notes, credential status when present, and error details.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
