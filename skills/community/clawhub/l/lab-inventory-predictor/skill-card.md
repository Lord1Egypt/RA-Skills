## Description:

Predict depletion time of critical lab reagents based on historical usage frequency, and automatically generate purchase alerts when stock falls below safety thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Lab operations staff and research teams use this skill to track reagent inventory, estimate depletion dates from usage history, and generate purchase or safety-stock alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inventory data paths can be user-selected, and security evidence says the script may read or overwrite JSON files despite documented workspace-only restrictions.

Mitigation: Run only with trusted, explicit inventory paths until the script enforces an approved workspace before opening or saving data.

Risk: Mutating actions can change inventory data, and reagent removal has no confirmation step.

Mitigation: Require operator review or confirmation before destructive inventory updates, especially removal actions and writes to existing JSON files.

Risk: The release includes an unnecessary dataclasses dependency for a Python 3.8+ standard-library feature.

Mitigation: Remove the dependency or install only from trusted package indexes in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/lab-inventory-predictor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text summaries with optional JSON report output from the bundled Python script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include assumptions, limits, missing inputs, and LOW_CONFIDENCE notes when sparse usage history affects prediction reliability.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
