## Description:

Collect invoices and receipts from Gmail, attach PDFs or screenshots when needed, and send a summary email to a configured recipient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mintannn](https://clawhub.ai/user/mintannn)

### License/Terms of Use:


## Use Case:

Employees and business users use this skill to gather invoice, receipt, and billing emails from Gmail for a date range, collect PDF attachments or screenshots, and forward a summary package to an accounting or operations recipient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access and forward sensitive Gmail invoice data.

Mitigation: Grant only the Gmail access needed for the intended account, restrict recipients, and review attachments or screenshots before sending.

Risk: Rendering email HTML with Chromium may expose the environment to malicious email content, especially when sandboxing is disabled.

Mitigation: Run screenshot rendering in an isolated environment with remote content and JavaScript blocked where possible.

Risk: Unpinned dependency installation can introduce supply-chain exposure.

Mitigation: Pin and verify gogcli and Puppeteer dependencies before use, including checksum verification for downloaded archives.

Risk: Recurring automation can repeatedly send invoices to the wrong destination if recipient or scope settings are incorrect.

Mitigation: Avoid enabling cron until recipient allowlists, search scopes, and review controls are in place.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mintannn/skills/invoice-collector)
- [Google Cloud Console](https://console.cloud.google.com/)
- [gogcli Linux Release Archive](https://github.com/steipete/gogcli/releases/latest/download/gogcli_linux_amd64.tar.gz)
- [gogcli Checksums](https://github.com/steipete/gogcli/releases/latest/download/checksums.txt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create PDF or PNG invoice artifacts and send a summary email via Gmail.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
