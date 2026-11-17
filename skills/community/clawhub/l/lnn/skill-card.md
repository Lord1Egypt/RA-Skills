## Description:

Builds, trains, and inspects Liquid Neural Networks using LTC and CfC models with NCP-style wirings on PyTorch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[promiseyuki](https://clawhub.ai/user/promiseyuki)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, train, evaluate, save, and inspect liquid neural network models for time-series prediction and continuous-time sequence modeling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing unpinned or newly resolved Python dependencies can introduce dependency risk.

Mitigation: Install in a virtual environment and review or pin ncps, torch, numpy, pandas, and optional matplotlib before use.

Risk: Training on untrusted CSV files can expose the workflow to malformed or unwanted local data inputs.

Mitigation: Use only trusted CSV files and verify selected feature and target columns before training.

Risk: Saved model and optional graph outputs write local files selected by the user.

Mitigation: Choose output paths deliberately and review generated .pt or PNG files before sharing or deploying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/promiseyuki/skills/lnn)
- [ncps documentation](https://ncps.readthedocs.io/en/latest/)
- [Liquid Neural Networks theory reference](references/lnn_theory.md)
- [ncps API cheatsheet](references/api_cheatsheet.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; local scripts can emit console metrics, saved PyTorch model files, and optional wiring graph images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on user-selected model, wiring, dataset, training steps, random seed, evaluation, rollout, save, and wiring inspection options.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
