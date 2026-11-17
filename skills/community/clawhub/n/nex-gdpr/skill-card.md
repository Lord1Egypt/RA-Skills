## Description:

Nex GDPR helps agency operators and data controllers register GDPR/AVG data subject requests, scan local OpenClaw-related data locations for personal data, generate exports and response letters, process erasure workflows, and maintain audit records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexaiguy](https://clawhub.ai/user/nexaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

Agency operators, data controllers, and organizations handling GDPR/AVG data subject requests use this skill to track request status, locate related personal data, prepare access or portability exports, record erasure actions, and generate compliance documentation.

### Deployment Geography for Use:

Belgium and European Economic Area (EEA) GDPR contexts

## Known Risks and Mitigations:

Risk: The skill can scan, export, and delete sensitive local data.

Mitigation: Use it only for authorized GDPR data processing, narrow scan paths with configuration, and review findings before processing requests.

Risk: Erasure processing can remove user-owned files.

Mitigation: Do not run erasure processing until backups exist and a reviewed deletion plan identifies what should be deleted or retained.

Risk: Exports and the ~/.nex-gdpr database may contain plaintext sensitive data.

Mitigation: Apply strict local permissions and add encryption or separate secure storage before retaining or transmitting exports.

## Reference(s):

- [Nex AI homepage](https://nex-ai.be)
- [ClawHub skill page](https://clawhub.ai/nexaiguy/skills/nex-gdpr)
- [ClawHub publisher profile](https://clawhub.ai/user/nexaiguy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, files]

**Output Format:** [Markdown guidance with inline shell commands, CLI text/table output, JSON reports, and ZIP export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When executed, commands can create local SQLite records and export artifacts under ~/.nex-gdpr.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
