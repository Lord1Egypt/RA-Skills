## Description:

Organizes and deduplicates locally exported bookmark or link lists, generating themed indexes and maintenance recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to review copied bookmark exports or tightly scoped link folders, identify duplicates and topics, and produce a Markdown maintenance plan before making changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included script can scan arbitrary local directories and report file names and Markdown headings.

Mitigation: Run it only on a copied bookmark export or a tightly scoped folder; avoid home directories, project roots, credential folders, and other sensitive locations.

Risk: Generated reports may expose sensitive bookmark, link, or local file metadata if shared.

Mitigation: Review and redact Markdown or JSON output before sending, publishing, or storing it outside the local workspace.

Risk: The skill is advertised as a bookmark organizer, but evidence says the script mainly performs local directory audit and reporting.

Mitigation: Treat outputs as review drafts and manually confirm any delete, merge, reclassification, or browser-change action before applying it elsewhere.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/local-bookmark-librarian)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)
- [Skill specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance, Shell commands]

**Output Format:** [Markdown reports or JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a report file when an output path is supplied; otherwise prints to stdout.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
