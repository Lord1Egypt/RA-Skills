## Description:

Deconstructs local insurance product document folders into structured, evidence-backed Markdown reports for an Obsidian product knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lzquinn](https://clawhub.ai/user/lzquinn)

### License/Terms of Use:

MIT-0

## Use Case:

Insurance advisors and knowledge-base maintainers use this skill to process local insurance product PDFs, spreadsheets, product manuals, rate tables, underwriting rules, and service documents into standardized Markdown product analysis for comparison and client preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can exceed the intended product-folder boundary through configured output paths or untrusted product folders.

Mitigation: Review config.json before use, set a deliberate output path, and run only on trusted product folders without symlinks.

Risk: Generated financial and contractual statements may be unsupported or misleading if extraction misses source evidence.

Mitigation: Treat reports as drafts and verify all product claims, calculations, and contract statements against the original documents before use.

Risk: Broad, unpinned Python dependencies increase supply-chain and runtime variability when processing untrusted files.

Mitigation: Pin and review dependency versions before using the skill on untrusted product folders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lzquinn/skills/insurance-product-deconstruction)
- [Publisher profile](https://clawhub.ai/user/lzquinn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with YAML frontmatter, evidence references, and inline shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes product reports to a configured Obsidian output path and uses local cached extraction artifacts.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
