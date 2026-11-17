## Description:

Build and maintain a compiled LLM Wiki inside an Obsidian vault by ingesting raw sources, compiling interlinked wiki pages, generating indexes, linting wiki health, and answering from compiled pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerome-benoit](https://clawhub.ai/user/jerome-benoit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to operate an Obsidian vault as a persistent compiled knowledge base. It supports source ingestion, wiki page generation, graph and index maintenance, linting, and querying previously compiled wiki content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned runtime package execution can occur when markdown structure checks use npx to run markdownlint-cli2.

Mitigation: Pin or preinstall markdownlint-cli2 before use, and review the skill before installing.

Risk: Vault path containment is imperfect for wiki-manifest.sh mark when untrusted file paths are passed.

Mitigation: Use an explicit trusted vault path and do not pass untrusted file paths to wiki-manifest.sh mark until canonical path containment is fixed.

Risk: Automatic fix workflows can modify wiki files in the selected vault.

Mitigation: Keep the vault under version control or backups and avoid --fix until changes can be reviewed or reverted.

## Reference(s):

- [Karpathy LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [agents-template.md](artifact/references/agents-template.md)
- [schema-template.md](artifact/references/schema-template.md)
- [taxonomy-template.md](artifact/references/taxonomy-template.md)
- [ClawHub skill page](https://clawhub.ai/jerome-benoit/skills/obsidian-wiki)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, wiki page content, configuration files, and generated reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and updates files inside a user-selected Obsidian vault when the workflow calls for setup, ingest, lint fix, graph export, or maintenance.]

## Skill Version(s):

1.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
