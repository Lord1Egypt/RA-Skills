## Description:

Queries Juhe mobile-number attribution data for Chinese mobile numbers or 7-digit prefixes, returning province, city, area code, postal code, carrier, and card type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up attribution details for Chinese mobile numbers or 7-digit prefixes and present the results as concise text or tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Phone numbers and the API key are sent to Juhe over unencrypted HTTP.

Mitigation: Change the lookup endpoint to verified HTTPS before using real phone numbers or a valuable API key.

Risk: Queried phone numbers are disclosed to the external Juhe service.

Mitigation: Use the skill only when users accept sending the numbers to Juhe, and avoid unnecessary full-number lookups.

Risk: Passing the API key on the command line or storing it in a shared .env file can expose the credential.

Mitigation: Prefer the JUHE_MOBILE_KEY environment variable and restrict access to any local key files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-mobile-locate)
- [Juhe mobile number API documentation](https://www.juhe.cn/docs/api/id/11)
- [Juhe data platform](https://www.juhe.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or terminal text with tabular lookup results and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Masks full phone numbers by default unless the user requests unmasked output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
