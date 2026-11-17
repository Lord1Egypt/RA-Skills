## Description:

Runs the GIGO Lobster benchmark in local mode, producing local reports and certificates without creating a personal result page or leaderboard entry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gigolab](https://clawhub.ai/user/gigolab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to run a 50-task agent benchmark locally and collect report, certificate, log, and score outputs without publishing ranking results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports that the skill advertises local-only benchmarking while inspected code can contact a remote API, send output for judging, download executable evaluators, and expose host secrets to benchmark processes.

Mitigation: Use only with explicit offline mode in a sandboxed account or container, remove secrets from the environment, and independently review or sign remote task bundles before trusting them.

Risk: Benchmark tasks can execute checks and evaluators against working directories that may contain sensitive project data.

Mitigation: Run the skill in a dedicated workspace with non-sensitive sample data and inspect generated reports and logs before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gigolab/skills/gigo-lobster-local)
- [Artifact skill instructions](artifact/SKILL.md)
- [Artifact README](artifact/README.md)
- [Benchmark bundle README](artifact/bundle/README.md)
- [Task schema](artifact/bundle/specs/task-schema.md)
- [Scoring specification](artifact/bundle/specs/scoring.md)
- [Judge protocol](artifact/bundle/specs/judge-protocol.md)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown progress updates with bash command invocation and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local benchmark artifacts such as lobster-report.html, lobster-cert.png or lobster-cert.svg, gigo-run.log, scores, and result references.]

## Skill Version(s):

2.1.2 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
