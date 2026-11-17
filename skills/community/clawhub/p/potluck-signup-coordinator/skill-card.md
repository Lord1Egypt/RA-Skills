## Description:

Design shared potluck and volunteer signups, reconcile claims and detect gaps. Prefer Google Sheets; support SignUpGenius packets/exports and provider-permitted browser workflows without requiring an API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jjjhenriksen](https://clawhub.ai/user/jjjhenriksen)

### License/Terms of Use:

MIT

## Use Case:

External event organizers use this skill to plan potluck and volunteer contribution slots, prepare signup materials, and reconcile current claims to identify gaps. It can support Google Sheets workflows and SignUpGenius packets or organizer-provided exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence is incomplete because one local reference could not be matched to a bundled artifact.

Mitigation: Check the bundled reference mapping before relying on the affected guidance.

Risk: Shared signup files could expose private guest or organizer information.

Mitigation: Keep shared content guest-safe and store private contacts and notes in a separate unshared file.

Risk: A partial signup snapshot can make an unobserved claim appear removed.

Mitigation: Treat missing claims as unknown unless the after snapshot is complete, and verify the current source before proposing changes.

Risk: Automated SignUpGenius use may not be permitted by the provider.

Mitigation: Use a manual signup packet or a verified permitted integration; do not automate site access without provider permission.

## Reference(s):

- [Google Sheets workflow guidance](references/google-sheets.md)
- [Offline reconciliation input contract](references/input.md)
- [SignUpGenius adapter limits](references/signupgenius.md)
- [Google Sheets API values guide](https://developers.google.com/workspace/sheets/api/guides/values)
- [Google Sheets API batch update guide](https://developers.google.com/workspace/sheets/api/guides/batchupdate)
- [SignUpGenius potluck guide](https://www.signupgenius.com/how-to-use/potluck)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, CSV, JSON]

**Output Format:** [Signup plans and reconciliation summaries in Markdown, with CSV templates and JSON snapshot reports where applicable.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reconciliation reflects supplied snapshots; partial snapshots cannot establish that missing claims were removed.]

## Skill Version(s):

0.1.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
