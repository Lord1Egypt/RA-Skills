## Description:

Scans popular GitHub Agent Skill repositories, builds a star-ranked candidate pool, analyzes representative SKILL.md design patterns, and produces China-market adaptation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junci003](https://clawhub.ai/user/junci003)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, and product researchers use this skill to benchmark GitHub Agent Skill examples, identify reusable design patterns, and create evidence-backed teardown reports with China-market adaptation recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the logged-in GitHub CLI account for read-only repository metadata and content collection.

Mitigation: Run it with the intended GitHub account and review the generated repository list before relying on the analysis.

Risk: The bundled scripts write local analysis artifacts under SKILL_OUT or the current working directory.

Mitigation: Set SKILL_OUT to a deliberate workspace and inspect generated files before sharing or publishing them.

Risk: Teardown conclusions depend on fetched repository content and may become stale as GitHub repositories or platform policies change.

Mitigation: Refresh the scans and verify quoted source material and policy-sensitive recommendations before business use.

## Reference(s):

- [Domestic adaptation reference](artifact/references/china-adaptation.md)
- [ClawHub skill page](https://clawhub.ai/junci003/skills/github-skill-teardown)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown teardown report plus JSON candidate pools and local analysis files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses GitHub CLI read-only API calls and writes local outputs under SKILL_OUT or the current working directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
