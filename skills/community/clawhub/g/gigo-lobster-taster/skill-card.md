## Description:

Gigo Lobster Taster runs the full OpenClaw lobster benchmark, uploads verified results by default, creates a personal result page, and enters the result on the leaderboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gigolab](https://clawhub.ai/user/gigolab)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and agent developers use this skill to run a multi-task agent benchmark, review local reports and certificates, and optionally publish verified results to a personal result page and leaderboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The benchmark may execute adversarial coding tasks with broad local environment access.

Mitigation: Run it in a disposable workspace or container with only the files and environment variables needed for the benchmark.

Risk: Default runs can upload complete agent answers and results to api.agent-gigo.com.

Mitigation: Use the local or skip-upload mode when responses or results should not be sent to the service.

Risk: Local caches, logs, reports, and certificates are created during execution.

Mitigation: Review the output directory and remove generated logs or artifacts that should not be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gigolab/skills/gigo-lobster-taster)
- [README](README.md)
- [GIGO Lobster Taster v2 task bundle](bundle/README.md)
- [Task schema](bundle/specs/task-schema.md)
- [Scoring](bundle/specs/scoring.md)
- [Judge protocol](bundle/specs/judge-protocol.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, configuration, guidance]

**Output Format:** [Markdown guidance with shell command invocations and generated local report, certificate, log, and result artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default runs may upload complete agent answers and benchmark results to api.agent-gigo.com; local and register-only modes alter publication behavior when explicitly selected.]

## Skill Version(s):

2.1.2 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
