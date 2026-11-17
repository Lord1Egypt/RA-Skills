## Description:

Helps analyze miRNA targets across supported or custom transcriptomes, annotate and enrich predicted genes, assess sequence conservation, and prepare figures and network exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[destinqu](https://clawhub.ai/user/destinqu)

### License/Terms of Use:

MIT

## Use Case:

Bioinformatics researchers and developers use this skill to predict and prioritize miRNA target genes, explore functional enrichment and conservation, and prepare analysis outputs for visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dependency installer can change system packages and build downloaded third-party code without integrity checks.

Mitigation: Run analysis in an isolated conda or container environment; prefer trusted package managers for dependencies and avoid running the installer on sensitive hosts.

Risk: Online annotation and enrichment may disclose submitted gene lists or sequences to third-party services.

Mitigation: Use online features only when sharing the input with third-party APIs is acceptable; keep sensitive or unpublished data local.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/destinqu/skills/mirna-target-tools)
- [Workflow guide](references/workflow.md)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Executed workflows can produce target and enrichment tables, FASTA alignments, figures, and Cytoscape network files.]

## Skill Version(s):

3.0.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
