## Description:

Knowledge Engine helps agents search, add, link, distill, and visualize a local personal knowledge base of concepts and beliefs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zabr1314](https://clawhub.ai/user/zabr1314)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to maintain a local personal knowledge system: searching and adding concepts, linking related ideas, tracking belief changes, distilling recurring patterns, and generating graph views.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores personal knowledge, beliefs, contexts, and search usage in local plaintext JSON files and SQLite.

Mitigation: Avoid highly sensitive material, restrict access to the local memory directory, and review stored data before sharing backups or generated outputs.

Risk: The visualization flow can expose knowledge graph content in HTML and currently depends on remote D3 loading.

Mitigation: Do not include sensitive content in graph visualizations until the dependency is vendored or pinned and the HTML rendering path is hardened.

Risk: Cleanup and pruning commands can remove or deprecate knowledge records.

Mitigation: Use the documented --dry-run option before pruning and keep backups of the local memory directory.

Risk: Mutable latest or head install commands can install code that differs from the reviewed release.

Mitigation: Prefer pinned installer versions or reviewed commits for installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zabr1314/skills/knowledge-engine)
- [README](artifact/README.md)
- [Concept Card Schema](artifact/resources/concept-schema.md)
- [Belief Card Schema](artifact/resources/belief-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Python snippets, plus local JSON, SQLite, Markdown, and HTML artifacts when the bundled scripts are run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores knowledge locally in plaintext JSON files and a SQLite index; visualization output is an HTML knowledge graph.]

## Skill Version(s):

0.3.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
