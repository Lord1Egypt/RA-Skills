## Description:

Find and send local files to a chat channel, including Telegram, Discord, WhatsApp, Signal, and Slack, and manage encrypted credential files with age encryption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lookupmark](https://clawhub.ai/user/lookupmark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to have an agent locate readable local files, confirm ambiguous paths, and send selected files through supported chat channels. It also provides workflows for encrypting, storing, decrypting, and sending credential files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local filesystem search and chat-based file transfer can expose sensitive local files to unauthorized recipients.

Mitigation: Install only with a verified recipient allowlist and restrict file searches to approved directories before use.

Risk: The skill's behavior grants chat requests broad authority to send sensitive documents and credentials.

Mitigation: Remove anti-refusal instructions and require explicit identity verification and confirmation before sending sensitive files or credentials.

Risk: Credential handling has temp-file and path-validation concerns identified by the server security evidence.

Mitigation: Fix credential temp-file handling and path validation before use, and verify plaintext artifacts are deleted after encryption or sending.

## Reference(s):

- [age file encryption](https://github.com/FiloSottile/age)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and file-transfer status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute local filesystem search, file staging, OpenClaw message sending, and age-based credential encryption or decryption when used by an agent.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
