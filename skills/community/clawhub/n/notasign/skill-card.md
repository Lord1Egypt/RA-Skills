## Description:

Send supported local files, uploaded attachments, or URLs for e-signature through Nota Sign in PROD or UAT while collecting signer details and required credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[notasign](https://clawhub.ai/user/notasign)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure Nota Sign credentials and send supported documents or URLs for signature to one or more signers through PROD or UAT.

### Deployment Geography for Use:

Global, with Nota Sign API regions CN, AP1, AP2, and EU1 selected during configuration.

## Known Risks and Mitigations:

Risk: The skill stores a Nota Sign signing private key in a local JSON config file.

Mitigation: Use a secret manager or strict file permissions, avoid local override files that may be synced or committed, and keep secrets out of normal responses.

Risk: The fallback execution path can download Node.js and tsx through unpinned npx commands.

Mitigation: Prefer a reviewed local Node.js 18+ runtime with pinned tooling, and review before allowing npm network access.

Risk: The skill uploads documents and signer data to Nota Sign endpoints.

Mitigation: Use it only with documents and recipient data the user is authorized to send, and confirm the target environment, region, and credentials before sending.

## Reference(s):

- [ClawHub Nota Sign skill page](https://clawhub.ai/notasign/skills/notasign)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns an envelope ID and send summary on success; surfaces validation or API errors on failure.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
