## Description:

Keep track of positions across any exchange, broker, or external system, detect orphans, prevent leaks, and reconcile state for stateful bots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to integrate self-healing position tracking into bots or services that must compare local state with an external exchange, broker, cloud provider, API service, database pool, or subscription system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional auto-close behavior can affect real financial, cloud, subscription, or other external resources.

Mitigation: Keep auto_close disabled until it has been tested with non-production data, explicit confirmation, allowlists, fresh re-checks, logging, and rollback expectations.

Risk: The user-provided API adapter determines what external systems the tracker can read from or modify.

Mitigation: Review and constrain adapter permissions before use, and run the skill from a pinned, hash-verified package or copied source file in a non-privileged virtual environment.

Risk: External state can change during reconciliation, creating false orphan or phantom detections.

Mitigation: Verify external state again before cleanup, tune reconciliation intervals for API limits, and prefer manual review until behavior is validated for the target system.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/theshadowrose/skills/position-tracker)
- [Publisher Profile](https://clawhub.ai/user/theshadowrose)
- [Known Limitations](LIMITATIONS.md)
- [Configuration Example](config_example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples, shell commands, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on integrating position_tracker.py with a user-provided external API adapter.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
