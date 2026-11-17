## Description:

Audit a NousResearch/hermes-agent checkout or fork for Hermes-specific runtime-contract drift, command-surface splits, memory/skill/gateway health, and agent architecture risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangrichao2020](https://clawhub.ai/user/huangrichao2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit Hermes Agent checkouts, forks, and deployment support repositories for runtime-contract drift, command-surface splits, memory and skill health, gateway readiness, and agent architecture risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run an unpinned external Python package on local repositories.

Mitigation: Install only if the `hermescheck` package and publisher are trusted; prefer a pinned, hash-verified version in a virtual environment or container.

Risk: Local repository scans and generated reports may expose details beyond the intended Hermes Agent checkout.

Mitigation: Run the scanner only against the intended checkout, avoid exposing unrelated credentials, and review generated reports before sharing them.

## Reference(s):

- [Hermes Agent Health Check skill page](https://clawhub.ai/huangrichao2020/skills/hermes-agent-health-check)
- [Publisher profile](https://clawhub.ai/user/huangrichao2020)
- [Report schema](references/report-schema.json)
- [Playbooks](references/playbooks.md)
- [Code-level anti-patterns](references/code-patterns.md)
- [hermescheck PyPI package](https://pypi.org/project/hermescheck/)
- [NousResearch Hermes Agent](https://github.com/NousResearch/hermes-agent)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands; the scanner can produce JSON, Markdown, and SARIF report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports use the hermescheck.report.v1 schema and include severity-ranked findings with ordered fix plans.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
