## Description:

Automates a pipeline that scans Reddit developer pain points, clusters them, scaffolds pip-installable CLI tools, and prepares GitHub publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minirr890112-byte](https://clawhub.ai/user/minirr890112-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn Reddit pain signals into candidate Python CLI packages through scanning, clustering, scaffolding, packaging, and publication steps. It is best suited to workflows where generated package ideas and publication actions receive human review before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow collects and processes Reddit content, which can include privacy-sensitive or terms-restricted material.

Mitigation: Confirm Reddit API usage complies with applicable terms and review collected content for privacy concerns before using it.

Risk: The workflow includes GitHub push and package publication behavior that can publish generated code externally.

Mitigation: Require explicit human approval before any GitHub push or package publication.

Risk: Generated CLI package ideas and code may be incorrect, unsafe, or unsuitable for release.

Mitigation: Review generated code, documentation, and package metadata before building or publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/minirr890112-byte/skills/pain-to-pip-package)
- [HermesMade GitHub homepage](https://github.com/minirr890112-byte/HermesMade)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated package files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose repository publication steps that require explicit human approval.]

## Skill Version(s):

1.1.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
