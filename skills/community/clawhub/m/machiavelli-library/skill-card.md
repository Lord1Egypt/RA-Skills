## Description:

A bilingual Chinese-English searchable library that helps an agent find and return Machiavelli source passages with citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niflhum](https://clawhub.ai/user/niflhum)

### License/Terms of Use:

MIT-0

## Use Case:

External users and researchers use this skill to ask questions about Machiavelli and receive concise, cited passages from indexed bilingual source material rather than analysis or persona-style advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-use setup pulls changing content from an unpinned personal GitHub repository into the active skill directory.

Mitigation: Review and pin a specific commit before installation, or copy only reviewed data into a separate data-only directory.

Risk: Search keywords that look like command options may affect the grep fallback behavior.

Mitigation: Avoid untrusted option-like keywords and harden the search wrapper before relying on arbitrary user-supplied search terms.

Risk: Some included biographies, studies, and user-provided translations may have separate copyright or source-quality considerations.

Mitigation: Confirm rights and source quality for non-public-domain or user-provided materials before broad redistribution or commercial use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/niflhum/skills/machiavelli-library)
- [Publisher Profile](https://clawhub.ai/user/niflhum)
- [README](README.md)
- [Catalog Index](catalog/catalog.json)
- [Search Guide](index/search-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with cited source passages and optional shell command fallback]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the most relevant 3-5 original passages when available; reports no match rather than fabricating text.]

## Skill Version(s):

1.1.0 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
