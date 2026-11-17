## Description:

Helps agents call, test, debug, and integrate the 跨境卫士客户端 API by using the bundled OpenAPI specification for endpoint discovery, request construction, authentication handling, parameter validation, curl generation, and response interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mosquitood](https://clawhub.ai/user/mosquitood)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to translate requests about the 跨境卫士客户端 API into concrete API calls, curl commands, parameter choices, and response summaries. It is most relevant when integrating or troubleshooting shop list, open, and close workflows described by the bundled OpenAPI file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports that the skill ships what appears to be a real app ID and app secret.

Mitigation: Install only after the publisher removes and rotates the embedded credentials; until then, treat bundled credentials as compromised and avoid using them.

Risk: The release evidence reports broad local credential lookup guidance.

Mitigation: Narrow credential lookup to service-specific variables and do not allow the skill to read unrelated local configuration.

Risk: Generated curl commands can send authenticated requests to the configured API endpoint.

Mitigation: Review every generated command, confirm the target base URL and headers, and redact secrets before sharing logs or debugging output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mosquitood/skills/kuajingvs)
- [OpenAPI Specification](artifact/references/openapi.yaml)
- [Authentication Notes](artifact/references/auth.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces request plans, curl commands, API response summaries, and authentication guidance; users should review commands and redact secrets before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
