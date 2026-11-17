## Description:

Provides agent guidance and scripts for Temu EU tax API workflows through the LinkFox gateway, including export reports, Galerie signatures, invoice queries and downloads, merchant report downloads, and merchant invoice uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to work with Temu EU tax and VAT-related Partner API tasks such as querying invoices, downloading invoice PDFs, uploading merchant invoices, and requesting monthly tax reports.

### Deployment Geography for Use:

Europe

## Known Risks and Mitigations:

Risk: The skill handles Temu and LinkFox credentials.

Mitigation: Install only in a trusted workspace, keep credentials private, and share access only with users authorized to operate the relevant Temu and LinkFox accounts.

Risk: Scripts may store sensitive token or API response data locally.

Mitigation: Use a private workspace, review saved response files before sharing project contents, and remove local token or response files when they are no longer needed.

Risk: Generic proxy scripts and endpoint override environment variables can broaden what the skill can call.

Mitigation: Prefer the specific tax workflow scripts, avoid generic proxy scripts unless required, and confirm endpoint override variables are unset or point to trusted services.

Risk: Onboarding payment commands can create purchase actions.

Mitigation: Require deliberate user approval before running payment-related onboarding commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-tax-eu)
- [API reference](references/api.md)
- [Temu access token guide](references/access-token.md)
- [Authorization flow](references/authorization-flow.md)
- [Partner EU tax interface catalog](references/partner-eu-catalog.md)
- [Tax API document index](references/apis/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts may save full JSON responses under a workspace linkfox data directory and print either full JSON or a summary depending on response size.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
