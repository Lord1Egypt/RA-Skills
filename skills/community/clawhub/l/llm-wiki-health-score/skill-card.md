## Description:

Audits and scores an Obsidian or personal knowledge base against an LLM Wiki architecture using structured scanning, semantic sampling, and script-validated final scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[debtvc2022](https://clawhub.ai/user/debtvc2022)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge-base maintainers, and agent operators use this skill to audit a local Obsidian-style vault, generate structural signals, complete evidence-backed semantic sampling, and produce a final LLM Wiki health score. It is suited for local knowledge management workflows that need repeatable scoring, report artifacts, and JSON output for automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the selected vault contents during local audit.

Mitigation: Point the skill at the smallest intended vault root and avoid including unrelated sensitive files in that root.

Risk: The skill can create report files and semantic scoring templates in the selected vault by default.

Mitigation: Use --no-artifacts for a read-only run, or set --artifact-dir and --out to a safe explicit location.

Risk: A preliminary structural scan is not a final integrated score until semantic sampling is supplied and validated.

Mitigation: Use the semantic_scores.json workflow and --require-final when automation needs a completed final score.

## Reference(s):

- [LLM Wiki Health Scoring Model](references/scoring_model.md)
- [Dimension Design Rationale](references/dimension_design_rationale.md)
- [Probe Questions](references/probe_questions.md)
- [ClawHub Skill Page](https://clawhub.ai/debtvc2022/skills/llm-wiki-health-score)
- [ClawHub Publisher Profile](https://clawhub.ai/user/debtvc2022)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown reports, JSON reports, semantic scoring JSON templates, and concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local audit artifacts under the selected vault's tool-specific llm-wiki-health directory unless run with no-artifacts or explicit output paths.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata version: 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
