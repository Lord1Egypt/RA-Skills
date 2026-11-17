## Description:

Use a self-hosted Open Instagram API server to read and reply to DMs, publish photos, inspect account activity, and perform Instagram actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cprite](https://clawhub.ai/user/cprite)

### License/Terms of Use:

MIT-0

## Use Case:

External developers use this skill to operate an Instagram account through a self-hosted API, including reading messages, browsing account activity, and carrying out account actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial and did not inspect the referenced server script or systemd service file; its overall confidence is medium.

Mitigation: Review the upstream server and service files before installing or enabling the service.

Risk: The scanner reported two low-probability external-transmission alerts associated with documented API requests.

Mitigation: Review the documented requests and use the self-hosted server in an environment trusted with the account session.

Risk: The setup uses session cookies and a bearer token to access the account.

Mitigation: Have the account owner export cookies; never request their password or print, log, or commit cookies.json or api_token.

Risk: Publishing, commenting, following, and messaging can affect other people or create lasting public changes; the skill notes that published posts cannot be deleted through this API.

Mitigation: Use a test account first and confirm before public or irreversible actions.

Risk: The project is unofficial, and automating an account may lead to account restrictions.

Mitigation: Pace account actions and avoid bulk messaging, mass-following, or frequent posting.

## Reference(s):

- [Open Instagram API project](https://github.com/cprite/open-instagram-api)
- [ClawHub release page](https://clawhub.ai/cprite/skills/open-instagram-api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls]

**Output Format:** [Markdown instructions with curl examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples target a self-hosted API server and an authenticated Instagram session.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
