## Description:

Autonomous research workflow agent for AI and scientific research that helps brainstorm research ideas, conduct literature reviews, design experiments, run analysis, and write up findings with logbox tracking and reproducibility-first practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amberljc](https://clawhub.ai/user/amberljc)

### License/Terms of Use:

MIT

## Use Case:

External researchers, research teams, and developers use this skill to manage an AI or scientific research project across brainstorming, literature review, experiment design, analysis, and writing. It helps maintain decision provenance, reproducibility artifacts, phase outputs, and checkpoints for research judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search the web, write project files, and run analysis commands, which may affect important research artifacts.

Mitigation: Use project-scoped installation, keep version control enabled, and review proposed file changes and commands before allowing them.

Risk: Analysis workflows may involve expensive compute or long-running experiments.

Mitigation: Review experiment plans, resource assumptions, and command invocations before approving large runs.

Risk: Research drafts, protocols, or analysis summaries could contain incorrect or misleading conclusions.

Mitigation: Require researcher review of claims, limitations, evidence maps, and reproducibility checklists before public release.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/amberljc/skills/meta-research)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Analysis phase guide](artifact/phases/analysis.md)
- [Literature review phase guide](artifact/phases/literature-review.md)
- [Experiment protocol template](artifact/templates/experiment-protocol.md)
- [Reproducibility checklist](artifact/templates/reproducibility-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance, project files, checklists, protocols, code snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains a LOGBOX decision trail and may create or update research artifacts during the workflow.]

## Skill Version(s):

2.5.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
