## Description:

Govern multi-agent, delegation, parallel-work, and speed-first tasks by converting requests into bounded lanes, minimal context capsules, deterministic gates, freshness checks, and usage reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinadu-ai](https://clawhub.ai/user/tinadu-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to structure bounded multi-agent work, assign independent lanes, preserve artifact freshness, and run deterministic checks before QA or final reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unbounded delegation can create duplicated work, stale reviews, or inconsistent outputs.

Mitigation: Use the documented agent caps, assign disjoint lanes, keep integration with the main agent, and bind QA to current build hashes.

Risk: Hashing or usage helpers can record metadata for any source paths the agent is asked to inspect.

Mitigation: Scope helper-script inputs to the files or directories needed for the run and avoid broad private directories unless that is intentional.

Risk: Subagent findings can be incorrect or misleading if accepted without validation.

Mitigation: Run deterministic gates first, require evidence-backed findings, and verify artifact freshness before integrating QA results.

## Reference(s):

- [Agent Contracts](references/agent-contracts.md)
- [Orchestration Policy](references/orchestration-policy.md)
- [Quality Gates](references/quality-gates.md)
- [Context Capsule Schema](assets/context-capsule.schema.json)
- [Run Manifest Schema](assets/run-manifest.schema.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON manifest or capsule records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON run manifests and context capsules when helper scripts are invoked.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
