## Description:

Low Altitude Guardian analyzes low-altitude drone and eVTOL emergency scenarios, ranks crises and response options with a P0-P4 safety priority model, and returns advisory decision recommendations without connecting to flight-control systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaalenwow](https://clawhub.ai/user/aaalenwow)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, operators, and safety reviewers use this skill to analyze unmanned-device emergency scenarios, compare response options, and generate incident or enterprise emergency-planning outputs for training and offline advisory review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advisory emergency guidance for drones or eVTOL systems could be mistaken for certified flight-control or dispatch automation.

Mitigation: Use only for simulation, training, or offline advisory review; keep certified systems and qualified human operators responsible for real-world flight decisions.

Risk: Autonomous-execution language and persistent learning or ingestion workflows lack strong controls.

Mitigation: Do not connect outputs to flight controllers, dispatch automation, or actuator-capable systems, and avoid untrusted learning or ingestion files until path validation, approval gates, template integrity checks, and explicit human-review controls are added.

## Reference(s):

- [Crisis Taxonomy](references/crisis_taxonomy.md)
- [Decision Priority Matrix](references/decision_priority_matrix.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Natural-language guidance with optional JSON structures, Markdown reports, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory only; does not produce actuator commands or connect to flight-control systems.]

## Skill Version(s):

0.3.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
