## Description:

Import CSV and vCard contacts, review email and phone duplicates, merge records, track follow-ups, and export an address book.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users can maintain a private local address book, review and resolve duplicate contacts, record follow-ups, and export contact data as CSV or vCard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local contact database and exported files can contain private personal information.

Mitigation: Keep the workspace database and exports private, and do not upload the .mochilab state folder with a skill package.

Risk: Applying a merge removes source contact records after moving their follow-ups to the selected target.

Mitigation: Review the merge conflicts and selected field values, and back up the contact records before merging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-contact-desk)
- [MochiLab homepage](https://mochilab.bz)
- [JSON actions reference](references/input.md)

## Skill Output:

**Output Type(s):** [JSON, CSV files, vCard files]

**Output Format:** [JSON action results and CSV or vCard contact exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contact data is stored in the active workspace; imports are limited to 5 MiB and 2,000 contacts.]

## Skill Version(s):

1.0.1 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
