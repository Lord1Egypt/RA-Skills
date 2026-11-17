## Description:

Use the oo CLI and OOMOL-connected Avochato account to retrieve contacts and messages, inspect account identity, send text messages, and create or update contacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to read Avochato contacts and messages and manage contact communications through a connected account. Sending a message or creating or updating a contact changes account data and should be confirmed with the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup uses remote installers and the deployed CLI build has not been verified.

Mitigation: Review and approve CLI setup separately, and verify the installer and release before execution.

Risk: CLI setup may make startup changes to agent skill directories.

Mitigation: During setup, use OO_SKILLS_SYNC_DISABLED=1 as documented to prevent startup writes to agent skill directories.

Risk: Sending messages or changing contacts affects the connected Avochato account, and OOMOL processes Avochato requests.

Mitigation: Retain user confirmation before sending a message or creating or updating a contact, and ensure the user expects OOMOL to process the requests.

## Reference(s):

- [Avochato API Documentation](https://www.avochato.com/docs)
- [Avochato](https://www.avochato.com/)
- [oo CLI Repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI Command Documentation](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI Installation Guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON payloads and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the connected Avochato account; send_message and upsert_contact change account state and require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
