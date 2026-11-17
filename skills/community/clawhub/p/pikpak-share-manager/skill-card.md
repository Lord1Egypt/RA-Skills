## Description:

Create, inspect and revoke PikPak share links in batches, with full preview before any change.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipiguai87-alt](https://clawhub.ai/user/pipiguai87-alt)

### License/Terms of Use:

MIT-0

## Use Case:

PikPak account operators use this skill to audit share links in batches, review available share metadata, and identify exact IDs for separately authorized manual account changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit reports and terminal output contain private share metadata.

Mitigation: Keep output and reports private, and write reports only to a user-approved location.

Risk: An untrusted PikPak CLI or execution environment could run unintended code or inherit unsafe settings.

Mitigation: Use a trusted local CLI and trusted PATH, interpreter, script, and parent directories; avoid untrusted CI, multi-tenant, or privileged services.

Risk: Live share response fields and manual account-change behavior remain unverified.

Mitigation: Review exact share IDs and impacts, check local PikPak command help, and obtain separate explicit authorization before manual creation or revocation; read back changes afterward.

## Reference(s):

- [PikPak Share Manager design notes](artifact/references/upstream-design.md)
- [PikPak connected-app quota](https://mypikpak.com/zh-CN/help-center/transfer_quota/connected_apps_quota)
- [PikPak WebDAV speed limits](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/speed_limit)
- [ClawHub release page](https://clawhub.ai/pipiguai87-alt/skills/pikpak-share-manager)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Guidance]

**Output Format:** [JSON share audit report with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports contain private share metadata; the audit script does not create or revoke shares or generate revocation commands.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
