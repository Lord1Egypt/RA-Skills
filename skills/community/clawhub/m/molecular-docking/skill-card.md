## Description:

Run and diagnose expert-grade protein-ligand molecular docking through SciMiner using Gnina, AutoDock Vina, PackDock, SurfDock, DiffDock, and fpocket for focused docking, engine selection, ensemble sampling, pose-pool analysis, clustering, physics checks, confidence grading, and multi-engine comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sciminer](https://clawhub.ai/user/sciminer)

### License/Terms of Use:

MIT-0

## Use Case:

External scientists, drug discovery researchers, and computational chemistry developers use this skill to run structured SciMiner docking workflows and produce auditable docking hypotheses rather than one-shot score rankings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated receptor and ligand uploads are sent according to mutable remote SciMiner API documentation, and the local artifact does not define a fixed destination allowlist or integrity check.

Mitigation: Use the skill only when SciMiner's documentation hosting and credential controls are trusted, confirm that uploaded molecular data may leave the environment, and enforce destination/origin checks outside the skill when possible.

Risk: SciMiner credentials may be exposed or over-scoped if handled outside the skill's runtime contract.

Mitigation: Use short-lived, narrowly scoped SciMiner credentials and do not print, persist, derive, or search for the injected SCIMINER_API_KEY.

## Reference(s):

- [ClawHub molecular-docking skill page](https://clawhub.ai/sciminer/skills/molecular-docking)
- [SciMiner tool API documentation](https://sciminer.tech/tool_api_files/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured audit summaries, tables, file/API provenance, and inline shell/API guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include representative coordinate artifacts, pose/score provenance tables, SciMiner task IDs, and history URLs when jobs are run.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
