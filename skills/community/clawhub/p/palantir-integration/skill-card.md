## Description:

Advanced text-based integration suite for Palantir Maven Smart System (MSS) that manages targets, Kanban workflow, CDE risk assessment, SIGINT intelligence fusion, asset assignment, strike logistics, BDA reporting, and pattern-of-life analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frequensy23-coder](https://clawhub.ai/user/frequensy23-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to translate text requests into MSS API-backed reports and workflow actions for target review, deconfliction, logistics, weather, SIGINT, and BDA tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles MSS API credentials and stores configuration in a local .env file.

Mitigation: Install only in controlled environments, use short-lived scoped credentials, treat .env and command logs as sensitive, rotate keys used during setup, and avoid shared machines.

Risk: The skill can perform strike-related workflow changes, including target approval and asset assignment, with weak local safeguards.

Mitigation: Rely on server-side authorization, approval, deconfliction, and audit controls before permitting workflow-changing actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frequensy23-coder/skills/palantir-integration)
- [Publisher profile](https://clawhub.ai/user/frequensy23-coder)
- [Default MSS API endpoint from artifact](https://mss.palantir.mil/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise Markdown-style tactical reports, JSON from selected target queries, and shell-command-backed configuration or workflow actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only interface; tool results may include target data, risk assessments, intelligence summaries, asset status, logistics, weather, deconfliction, or workflow updates.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
