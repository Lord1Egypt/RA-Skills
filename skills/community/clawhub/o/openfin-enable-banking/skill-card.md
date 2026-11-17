## Description:

Connects DACH bank accounts through the Enable Banking API so an agent can onboard mandants, fetch balances and transactions, and renew sessions for tax advisory automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppronobis](https://clawhub.ai/user/ppronobis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance or tax automation teams use this skill to connect German and Austrian bank accounts, retrieve structured account data, and maintain Enable Banking sessions across multiple mandants.

### Deployment Geography for Use:

Germany and Austria

## Known Risks and Mitigations:

Risk: The callback server and local storage flow could expose sensitive financial data if run in an untrusted or publicly exposed environment.

Mitigation: Run only in a trusted environment, avoid public exposure of the callback server unless state validation and path handling are reviewed, and protect stored mandant and data JSON files as sensitive financial records.

Risk: Authorization links and callback codes can grant access to bank session setup if mishandled.

Mitigation: Do not forward authorization links through casual messaging channels; use controlled channels and prefer manual code handling when appropriate.

## Reference(s):

- [Enable Banking API Quick Reference](references/api-reference.md)
- [Enable Banking API Reference](https://enablebanking.com/docs/api/reference/)
- [ClawHub Skill Page](https://clawhub.ai/ppronobis/skills/openfin-enable-banking)
- [Publisher Profile](https://clawhub.ai/user/ppronobis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with bash commands and structured JSON data outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts can write mandant session records, pending callback codes, and fetched account data as local JSON files.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
