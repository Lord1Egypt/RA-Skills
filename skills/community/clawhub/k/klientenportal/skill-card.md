## Description:

Automate RZL Klientenportal.at, a web-based portal by RZL Software for exchanging receipts, invoices, and reports with a tax accountant, including login/logout, document upload, released-file listing, and Kanzleidokumente download through Playwright.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to automate routine RZL Klientenportal document exchange with a tax accountant, including uploading accounting documents, listing released or received files, and downloading portal documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles tax-portal credentials and accounting documents.

Mitigation: Install only in trusted workspaces, prefer short-lived environment variables or a secret manager, and keep any config file out of version control.

Risk: Uploaded or downloaded files may contain sensitive financial records.

Mitigation: Review files before upload and store downloads in a private directory.

Risk: A persistent browser session can remain after portal automation.

Mitigation: Run the logout command after use to clear the browser session.

Risk: Changing the portal URL can redirect automation away from the expected Klientenportal instance.

Mitigation: Use the derived portal URL from the portal ID and do not add a custom portal_url unless it has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/odrobnik/skills/klientenportal)
- [Klientenportal.at](https://klientenportal.at)
- [RZL Software](https://www.rzl.at)
- [Setup](SETUP.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text, JSON, Files]

**Output Format:** [CLI text, optional JSON listings, and downloaded portal files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, Playwright with Chromium, and Klientenportal credentials supplied through environment variables or a private config file.]

## Skill Version(s):

1.5.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
