## Description:

A temporary email assistant for creating disposable addresses and retrieving message lists and details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to create temporary email addresses and retrieve messages, including for email verification workflows and automated testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rates the skill suspicious due to a mismatch with its temporary-email purpose, broad request routing, unrelated fallback routes, and an unpinned installation command; the scan is incomplete because two references were unresolved.

Mitigation: Hold off on installation until the purpose mismatch and unrelated routes are clarified, review the unresolved references, and pin a reviewed release.

Risk: The skill requires a MaxHub API key to make requests.

Mitigation: Keep the key in the configured secret or environment variable and do not include its value in prompts or responses.

## Reference(s):

- [Source repository](https://github.com/XieWxx/maxhub-temp-mail)
- [MaxHub API and account site](https://www.aconfig.cn)
- [Email Operations API reference](artifact/references/api-email.md)
- [Parameter Mapping Reference](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown summaries and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports English and Chinese responses.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
