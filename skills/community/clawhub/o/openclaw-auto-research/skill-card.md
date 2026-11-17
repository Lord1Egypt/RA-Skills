## Description:

Auto Research Pipeline is an OpenClaw-native workflow that takes a research topic through 23 staged phases to produce a complete paper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lixiang1076](https://clawhub.ai/user/lixiang1076)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to coordinate a staged research workflow from topic scoping through literature review, experiment design, execution, analysis, paper writing, and citation verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute generated Python experiment code.

Mitigation: Run Phase E only in a disposable, network-restricted sandbox and review generated experiment code before execution.

Risk: The workflow writes persistent run artifacts and stores lessons for later runs.

Mitigation: Use a workspace without secrets or private files and review saved artifacts before retaining or sharing them.

Risk: The workflow can use external paper-search services and send phase summaries through Feishu.

Mitigation: Avoid sensitive research inputs unless external service use and notification routing are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lixiang1076/skills/openclaw-auto-research)
- [SKILL.md](artifact/SKILL.md)
- [Domain definitions](artifact/references/domains.yaml)
- [Phase A: Research Scoping](artifact/references/phase-a-scoping.md)
- [Phase B: Literature Discovery](artifact/references/phase-b-literature.md)
- [Phase C: Knowledge Synthesis](artifact/references/phase-c-synthesis.md)
- [Phase D: Experiment Design](artifact/references/phase-d-design.md)
- [Phase E: Experiment Execution](artifact/references/phase-e-execution.md)
- [Phase F: Analysis and Decision](artifact/references/phase-f-analysis.md)
- [Phase G: Paper Writing](artifact/references/phase-g-writing.md)
- [Phase H: Finalization](artifact/references/phase-h-finalize.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, YAML, BibTeX, LaTeX, and Python files written across staged run artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent per-run artifacts, including checkpoints, stage history, literature candidates, experiment files, analysis reports, paper drafts, and citation verification outputs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
