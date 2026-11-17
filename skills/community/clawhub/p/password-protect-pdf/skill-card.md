## Description:

Add password protection to a PDF by uploading it to the Solutions API, polling until completion, then returning a download URL for the protected PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crossservicesolutions](https://clawhub.ai/user/crossservicesolutions)

### License/Terms of Use:

MIT

## Use Case:

Developers, document operations teams, and agents use this skill to submit a PDF and password to the Solutions API, poll for completion, and retrieve the password-protected PDF download URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive PDFs, chosen passwords, and bearer tokens are sent to an external service.

Mitigation: Use only for documents and credentials approved for that service; avoid confidential PDFs and reused passwords.

Risk: Command-line secrets or untrusted base URL overrides can expose tokens or route data to an unintended destination.

Mitigation: Prefer SOLUTIONS_API_KEY over command-line tokens and use SOLUTIONS_BASE_URL or --base-url only after validating the destination.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crossservicesolutions/skills/password-protect-pdf)
- [Cross-Service-Solutions API registration](https://login.cross-service-solutions.com/register)
- [Solutions API base endpoint](https://api.xss-cross-service-solutions.com/solutions/solutions)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [JSON result with job status, file name, and protected PDF download URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PDF file, password, and Solutions API bearer token; processing occurs through an external API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
