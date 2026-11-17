## Description:

Runs the GIGO Lobster benchmark in share-page mode, generating a personal result page and certificate without entering the leaderboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gigolab](https://clawhub.ai/user/gigolab)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to run the GIGO Lobster agent benchmark, register a personal share page, and produce local result artifacts without opting into the public leaderboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a long benchmark and may execute benchmark tasks that modify temporary workspaces.

Mitigation: Run it in a dedicated workspace and review the generated log, report, and certificate before sharing results.

Risk: The register mode contacts the GIGO API and sends benchmark responses and results to create a share page.

Mitigation: Use this mode only when sharing benchmark results is acceptable, and avoid running it on sensitive prompts or private work.

Risk: Security evidence says the skill can read local profile data such as SOUL.md and may load broad local secrets.

Mitigation: Keep unrelated API keys out of the OpenClaw secrets environment and run with minimal local profile data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gigolab/skills/gigo-lobster-register)
- [Publisher Profile](https://clawhub.ai/user/gigolab)
- [README](artifact/README.md)
- [GIGO Lobster Taster v2 Bundle README](artifact/bundle/README.md)
- [Integration Guide](artifact/bundle/INTEGRATION.md)
- [Task Schema](artifact/bundle/specs/task-schema.md)
- [Scoring Specification](artifact/bundle/specs/scoring.md)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Text, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated local report, certificate, and log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a long benchmark and writes outputs under the configured OpenClaw workspace output directory.]

## Skill Version(s):

2.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
