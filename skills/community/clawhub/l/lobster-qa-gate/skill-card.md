## Description:

Qa Gate is a quality-check workflow for agents to validate documents, skills, PRDs, blog posts, and code artifacts for factual accuracy, tone consistency, completeness, structural integrity, operational soundness, and sensitive data handling before review or release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freeman88-tch](https://clawhub.ai/user/freeman88-tch)

### License/Terms of Use:

MIT-0

## Use Case:

Agents, developers, and content authors use this skill as a pre-release QA gate to inspect artifacts and produce a pass, pass-with-fixes, or fail verdict with severity-tagged findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill may be invoked broadly by phrases such as proofread or final check.

Mitigation: Invoke it explicitly for release gating and confirm the agent is expected to run a QA workflow before acting on findings.

Risk: The security evidence says the skill's read-only promise conflicts with behavior that can create QA report files and lead to artifact edits after a failed gate.

Mitigation: Run it only in workspaces where report creation and follow-up edits are acceptable, and review any proposed changes before accepting them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freeman88-tch/skills/lobster-qa-gate)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, files]

**Output Format:** [Markdown QA report with a PASS, PASS WITH FIXES, or FAIL verdict and severity-tagged findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write report files under qa-gate/YYYY-MM-DD-<artifact-slug>.md; failed gates can lead the agent to make corrections and re-run validation.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
