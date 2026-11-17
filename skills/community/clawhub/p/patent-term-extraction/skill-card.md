## Description:

Extract technical terms, acronyms, and source definitions from supplied patent texts, with cited passages and clearly separated suggested translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, patent researchers, and translation teams use this skill to build traceable glossaries of technical terms, acronyms, and definitions from supplied patent documents. It preserves source excerpts and separates suggested translations from terms stated in the original.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent retrieval can incur charges, and the client has no default spending cap while it may reuse an existing PatentMax key.

Mitigation: Agree on the document list and spending limit before retrieval; require a separate request before broadening searches.

Risk: A stored PatentMax key could be exposed on a shared computer or through an inadequately protected user directory.

Mitigation: Keep the ~/.patentmax directory private, especially on shared or Windows computers.

Risk: Suggested translations may not be authoritative terminology.

Mitigation: Keep the source term and cited passage visible, label translations as suggestions, and flag items that need verification.

## Reference(s):

- [PatentMax API reference](artifact/references/api-reference.md)
- [Patent search query syntax](artifact/references/query-syntax.md)
- [Patent search workflow](artifact/references/search-workflow.md)

## Skill Output:

**Output Type(s):** [Files, CSV, Guidance]

**Output Format:** [UTF-8 with BOM CSV glossary plus a concise accompanying summary and missing-material notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Entries retain cited source passages; original terms and suggested translations are distinguished, and unresolved items are flagged for review.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
