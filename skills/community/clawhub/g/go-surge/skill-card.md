## Description:

Guides Go code that uses the unofficial Surge SMS API client to manage messaging and related resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to add or update Go code that calls the Surge SMS API for messaging and account, contact, campaign, phone number, and verification operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Message and blast sending, verification creation, phone number purchases or releases, and account or contact changes can affect live Surge resources.

Mitigation: Perform these operations only when requested, and confirm the account and intended changes before sending write requests.

Risk: The Surge API bearer token could be exposed if it is hardcoded, committed, or logged.

Mitigation: Read the token from SURGE_API_KEY and never hardcode, commit, or log the token or Authorization header.

Risk: Webhook payload models are provided, but the client does not verify webhook signatures.

Mitigation: Verify webhook signatures in the receiving service before trusting payloads.

## Reference(s):

- [Setup and API usage reference](artifact/references/setup.md)
- [go-surge package documentation](https://pkg.go.dev/github.com/psyb0t/go-surge)
- [Project homepage](https://github.com/psyb0t/go-surge)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go examples, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.4.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
