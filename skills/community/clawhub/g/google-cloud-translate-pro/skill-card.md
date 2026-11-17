## Description:

Helps agents translate text, detect source languages, bulk translate inputs, and list supported language codes through a SocketsIO translation API wrapper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[q2408808](https://clawhub.ai/user/q2408808)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add multilingual translation, language detection, bulk translation, and supported-language lookup to agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is Google-branded, but server security evidence says its actual data flow uses SocketsIO.

Mitigation: Treat this as a SocketsIO translation client and review whether SocketsIO is approved before sending sensitive, regulated, or confidential text.

Risk: Changing SOCKETSIO_API_BASE can redirect submitted text and API keys to another endpoint.

Mitigation: Do not set SOCKETSIO_API_BASE unless the endpoint is fully controlled and approved for the submitted data.

## Reference(s):

- [Supported Language Codes](references/language-codes.md)
- [SocketsIO API Docs](https://socketsio.com/docs)
- [SocketsIO Pricing](https://socketsio.com/pricing)
- [ClawHub Skill Page](https://clawhub.ai/q2408808/skills/google-cloud-translate-pro)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text translations, detected-language lines, language-code lists, and Markdown command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SOCKETSIO_API_KEY. SOCKETSIO_API_BASE can redirect requests and should only be used with a trusted endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
