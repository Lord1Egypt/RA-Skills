## Description:

Saves paper metadata, links, optional abstracts, summaries, tags, and arXiv PDFs to a user's Zotero library using configured Zotero credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[little-cat1](https://clawhub.ai/user/little-cat1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research assistants use this skill to add scholarly paper records to Zotero from command-line inputs, including title, authors, URL, abstract, summary, and tags. It is useful for automating literature intake while preserving Zotero as the system of record.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Zotero API key that can create items, notes, and attachments in the configured library.

Mitigation: Use a limited Zotero key where possible and avoid sharing or committing ZOTERO_CREDENTIALS.

Risk: The bundled script can modify the user's Zotero library by creating records, notes, and attachments.

Mitigation: Review paper metadata and target credentials before execution, then verify created records in Zotero after running.

Risk: PDF download and upload behavior relies on paper URLs with weak validation.

Mitigation: Use trusted paper URLs and avoid passing untrusted or unexpected URLs to the script.

Risk: The script resolves an unpinned pyzotero dependency at runtime.

Mitigation: Pin and review dependencies before using the skill in a managed or production workflow.

## Reference(s):

- [Zotero](https://www.zotero.org)
- [ClawHub release page](https://clawhub.ai/little-cat1/skills/openclaw-zotero-scholar)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and Zotero library changes produced by the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and ZOTERO_CREDENTIALS; can create Zotero items, notes, and attachments.]

## Skill Version(s):

0.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
