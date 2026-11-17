## Description:

Supports CS PhD research projects with literature search, paper drafting, experiment planning, proof tracking, novelty checks, and pre-submission audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yue123161](https://clawhub.ai/user/yue123161)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and graduate students use this skill to organize theory or empirical projects, search academic sources, prepare draft materials, track evidence, and identify gaps before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and claims may be sent to third-party academic APIs.

Mitigation: Do not submit confidential research details in external searches.

Risk: Certificate or packaging commands may execute user-provided scripts.

Mitigation: Review scripts before running them; do not execute untrusted code.

Risk: Project commands write files into selected output directories.

Mitigation: Keep generated outputs in a designated project workspace and review destination paths.

## Reference(s):

- [ClawHub release](https://clawhub.ai/yue123161/skills/phd-research-companion)
- [Integrity workflow](references/integrity-workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance and commands; generated BibTeX, LaTeX, JSON, YAML, and HTML project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and audit results identify unavailable sources, missing evidence, and unresolved claims.]

## Skill Version(s):

1.0.3 (source: server-resolved ClawHub release; bundled documentation labels itself 2.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
