## Description:

Looks up Chinese enterprise restricted-consumption order records through the Juhe API by company name, unified social credit code, registration number, or applicant, and returns case, court, filing-date, status, related-person, applicant, and order-text details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check whether a Chinese enterprise or related applicant has court restricted-consumption records. It supports workflows that need case number, executing court, filing date, current or historical disclosure status, related person, applicant, and optional order text from Juhe.

### Deployment Geography for Use:

Global, subject to Juhe account eligibility and applicable local compliance requirements.

## Known Risks and Mitigations:

Risk: Enterprise, applicant, and case lookup terms are sent to Juhe for processing and billing.

Mitigation: Use the skill only when the user intends a Juhe lookup, disclose that query details are sent to Juhe, and avoid submitting unnecessary sensitive details.

Risk: The Juhe API key can be exposed if passed on the command line or stored in an unprotected .env file.

Mitigation: Prefer the JUHE_ENTERPRISE_RESTRICTION_KEY environment variable or a managed secret, keep scripts/.env out of version control, and restrict file access.

Risk: Results may include historical records, including records marked as no longer publicly disclosed.

Mitigation: Label current versus historical disclosure status in responses and request order text only when needed.

## Reference(s):

- [Juhe Enterprise Restricted Consumption API Documentation](https://www.juhe.cn/docs/api/id/836)
- [Juhe Data Platform](https://www.juhe.cn)
- [Juhe query836 API Endpoint](https://apis.juhe.cn/api_credit/query836)
- [ClawHub Skill Page](https://clawhub.ai/juhemcp/skills/juhe-enterprise-restriction)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text query summary with JSON result data and optional shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Juhe API key; sends lookup terms to Juhe; supports pagination with page size up to 200.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
