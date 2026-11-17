## Description:

Safely use a user's private local personal profile to help fill registration, signup, checkout, banking, KYC, and onboarding forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeguooooo](https://clawhub.ai/user/leeguooooo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to fill registration, checkout, banking, KYC, onboarding, and login forms from a private local or synced profile while preserving redaction, consent, and submit approval controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles highly sensitive identity, payment, banking, document, and password-vault data.

Mitigation: Use redacted summaries by default, reveal raw values only when required for the active form, and require explicit user confirmation before filling sensitive fields.

Risk: Automatic setup or profile-management actions could affect local software, vault configuration, synced folders, or source files.

Mitigation: Require explicit approval before software installation, vault setup, saving new sensitive fields, moving documents into iCloud or another sync folder, or deleting source files.

Risk: Autofill, credential entry, document upload, or final submission on an incorrect or suspicious site could expose private data.

Mitigation: Verify the real domain and form purpose before filling, stop on suspicious or typosquatted domains, and wait for explicit approval before uploads or final submit actions.

## Reference(s):

- [Source repository](https://github.com/leeguooooo/profile-use)
- [ClawHub skill page](https://clawhub.ai/leeguooooo/skills/profile-use)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and redacted summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include redacted summaries; high-sensitivity raw values are retrieved only for approved filling steps.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
