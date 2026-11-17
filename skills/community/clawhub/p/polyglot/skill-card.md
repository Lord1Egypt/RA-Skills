## Description:

Translate text into a language the user names, through AIProx (aiprox.dev): one POST /v1/translate for 40 sats (up to 6,000 characters), paid in Bitcoin Lightning (L402 or a LightningProx spend token). Detects the source language. Use it when the user asks for a translation and agrees to pay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec)

### License/Terms of Use:

MIT-0

## Use Case:

External users who need a text translation use Polyglot to translate up to 6,000 characters into a language they specify and receive the detected source language. Each request costs 40 sats and requires user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text sent for translation is shared with AIProx and its disclosed LightningProx processing service; retention was not independently verified.

Mitigation: Submit only text you are comfortable sharing, and exclude secrets and personal data.

Risk: A LightningProx spend token is a bearer credential, and each translation costs 40 sats.

Mitigation: Confirm the charge before each request and use a minimally funded token or an individual Lightning invoice.

## Reference(s):

- [AIProx](https://aiprox.dev)
- [AIProx API documentation](https://aiprox.dev/docs.html)
- [Translation API endpoint](https://aiprox.dev/v1/translate)
- [LightningProx spend token top-up](https://lightningprox.com/topup)
- [AIProx trial](https://aiprox.dev/start)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text translation with detected source language]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Input is limited to 6,000 characters and requires a target language.]

## Skill Version(s):

2.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
