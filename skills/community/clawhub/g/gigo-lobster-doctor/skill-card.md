## Description:

Gigo Lobster Doctor checks whether an OpenClaw environment can reach the gateway, satisfy Python runtime dependencies, access the task bundle, and generate PNG certificates without running the full benchmark.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gigolab](https://clawhub.ai/user/gigolab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill before a GIGO Lobster evaluation to verify local setup, task-bundle access, output writing, and certificate readiness while avoiding a full benchmark run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The doctor check may create a local Python runtime and install packages.

Mitigation: Run it in an isolated OpenClaw workspace or container and review the resolved package environment before broader use.

Risk: The skill may read OpenClaw secrets.env into the process environment.

Mitigation: Use a workspace with only the minimum required secrets and avoid running it in directories that contain unrelated credentials.

Risk: The skill contacts api.agent-gigo.com and fetches task bundle metadata.

Mitigation: Allow network access only when that service is expected, and use offline mode or network controls when remote checks are not desired.

Risk: The skill writes logs and output checks to the local output directory.

Mitigation: Choose an output directory that is safe for generated logs and review gigo-run.log before sharing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gigolab/skills/gigo-lobster-doctor)
- [Skill instructions](artifact/SKILL.md)
- [GIGO Lobster skill family README](artifact/README.md)
- [Task bundle README](artifact/bundle/README.md)
- [Task bundle integration guide](artifact/bundle/INTEGRATION.md)
- [Task schema](artifact/bundle/specs/task-schema.md)
- [Evaluator types](artifact/bundle/specs/evaluator-types.md)
- [Scoring specification](artifact/bundle/specs/scoring.md)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Terminal status text with a run log file and environment readiness guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default doctor mode does not run the full benchmark or upload leaderboard results; it may write gigo-run.log and temporary output-directory checks.]

## Skill Version(s):

2.1.2 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
