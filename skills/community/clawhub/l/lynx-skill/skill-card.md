## Description:

Stateless Go CLI for the Lynx Reservations travel agency system that lets an agent search files, retrieve itineraries, upload attachments, and manage documents with valid Lynx credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fredguile](https://clawhub.ai/user/fredguile)

### License/Terms of Use:

MIT-0

## Use Case:

Travel operations staff and agents use this skill to run Lynx Reservations CLI commands for file search, itinerary retrieval, document lookup, attachment upload, and file or transaction document updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live Lynx credentials and account-scoped travel data.

Mitigation: Install only from trusted publishers, use least-privilege Lynx account access, avoid plaintext .env files, and keep credentials out of logs and shared terminals.

Risk: Document save and attachment upload commands can mutate travel records.

Mitigation: Review command arguments before execution and confirm the target file, transaction, document type, and attachment path match the intended record.

Risk: Debug or environment inspection can expose credentials or sensitive request data.

Mitigation: Do not run broad environment dumps such as env | grep LYNX, and leave LYNX_DEBUG unset unless using a private machine with a plan to securely remove debug files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fredguile/skills/lynx-skill)
- [Lynx Reservations](https://www.lynx-reservations.com/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Lynx credentials in LYNX_USERNAME, LYNX_PASSWORD, and LYNX_COMPANY_CODE.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
