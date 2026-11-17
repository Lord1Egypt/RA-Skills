## Description:

Let your AI agent interact with Hashmob.net.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ibnaleem](https://clawhub.ai/user/ibnaleem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security practitioners use this skill to have an agent look up HashMob API routes and prepare curl commands for public API queries and approved account-authenticated actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated HashMob API calls can submit hashes, manage hashlists, change account settings, make purchases, run paid searches, or initiate withdrawals.

Mitigation: Require explicit human approval before any authenticated, paid, destructive, withdrawal, purchase, submission, preference, notification, or hashlist-management action.

Risk: The security review notes that the skill under-warns about account-changing and destructive actions that could affect user data or account value.

Mitigation: Review the target endpoint and HashMob's real authorization requirements before execution, especially for endpoints marked as requiring no API key.

Risk: The HASHMOB_API_KEY grants access to the user's HashMob account.

Mitigation: Treat the API key like a password, avoid exposing it in logs or shared transcripts, and only pass it to approved HashMob API requests.

## Reference(s):

- [HashMob](https://hashmob.net)
- [HashMob API v2 Documentation](https://hashmob.net/docs/api-v2-docs.json)
- [Hashcat Wiki](https://hashcat.net/wiki/)
- [ClawHub Skill Page](https://clawhub.ai/ibnaleem/skills/hashmob)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration guidance]

**Output Format:** [Markdown with curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; authenticated examples use HASHMOB_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
