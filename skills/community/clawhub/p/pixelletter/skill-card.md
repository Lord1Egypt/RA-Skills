## Description:

Send letters, PDFs, postcards, faxes, or query PixelLetter account credit via the PixelLetter HTTPS API with automated physical mail dispatch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bone187](https://clawhub.ai/user/bone187)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent prepare, dry-run, and, after explicit confirmation, send PixelLetter letters, PDFs, faxes, registered mail, or account-balance requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An endpoint override can redirect PixelLetter credentials and documents away from the default PixelLetter service.

Mitigation: Use the default PixelLetter endpoint and do not set PIXELLETTER_ENDPOINT unless the destination has been audited.

Risk: Production sends can spend account credit and dispatch real postal mail or faxes.

Mitigation: Use dry-run or test mode first, then require explicit confirmation of recipient, document, options, cost intent, --production, --confirm-real-send, and PIXELLETTER_ALLOW_REAL_SEND=true before any real send.

Risk: Dry-run or raw output can expose private correspondence details even when credentials are redacted.

Mitigation: Avoid sharing command output, logs, screenshots, or examples that contain recipient addresses, document text, transaction details, or raw API responses.

## Reference(s):

- [PixelLetter HTTPS API Notes](references/api.md)
- [PixelLetter](https://www.pixelletter.de)
- [PixelLetter Error Messages](https://www.pixelletter.de/docs/error_messages.php)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call an external HTTPS API; dry-run prints sanitized XML and production sends require explicit confirmation flags.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
