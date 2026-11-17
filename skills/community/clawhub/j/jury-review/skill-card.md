## Description:

Jury Review guides agents through a Chinese-language, role-based review workflow for multi-dimensional code scoring, edge-case challenge roles, and iterative improvement feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kukuxnd](https://clawhub.ai/user/kukuxnd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to structure code review tasks into role-based evaluation rounds, weighted scoring, edge-case challenges, and actionable improvement feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled scorer reads code files supplied for scoring.

Mitigation: Run it only on files intended for review and avoid passing sensitive code unless that review is approved.

Risk: The scoring workflow and local scorer are lightweight heuristics and may miss defects or security issues.

Mitigation: Use the output as review guidance alongside normal testing, security scanning, and human review.

## Reference(s):

- [Scoring Guide](references/scoring-guide.md)
- [AutoResearch](https://github.com/karpathy/autoresearch)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown review reports with optional JSON scoring output from the bundled local scorer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces role-based scores, issue summaries, challenge feedback, and iteration decisions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
