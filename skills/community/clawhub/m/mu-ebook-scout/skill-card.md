## Description:

Multi-source ebook search across public-domain classics, Chinese text sources, LibriVox audiobooks, community netdisk book lists, and Google Books metadata for users looking for ebooks, EPUB/PDF/MOBI files, or audiobooks in Chinese or English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muippt](https://clawhub.ai/user/muippt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search for ebooks or audiobooks, rank legal reading and download options, and return readable links or source-specific next steps. Downloads are only appropriate after explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Community netdisk retrieval can surface copyrighted or unauthorized files.

Mitigation: Prefer public-domain, open-license, borrow, purchase, or official reading links; avoid fetching copyrighted works from unofficial hosts.

Risk: Agent-assisted downloads from netdisk hosts may retrieve untrusted archives or unsafe files.

Mitigation: Require explicit user consent, download only in a constrained workspace, verify archive and file formats, and avoid unpacking untrusted archives outside that environment.

Risk: Automated downloading may exceed the user's intent or normalize batch collection.

Mitigation: Wait for an unambiguous request for a specific item and do not pre-download or batch-download results.

## Reference(s):

- [ctfile direct-link playbook](references/ctfile-playbook.md)
- [ClawHub skill page](https://clawhub.ai/muippt/skills/mu-ebook-scout)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with ranked result summaries, links, and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include direct download or deep links only after explicit user confirmation; netdisk results should remain link-only unless the user asks for agent-assisted retrieval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
