## Description:

Complete machine learning pipeline for trading: feature engineering, AutoML, deep learning, and financial RL for automated parameter sweeps, feature creation, model training, and anti-leakage validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahuserious](https://clawhub.ai/user/ahuserious)

### License/Terms of Use:


## Use Case:

Developers and quantitative trading researchers use this skill to plan, audit, and implement ML feature engineering and model pipelines, including data validation, anti-leakage checks, model evaluation, and deployment artifact preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill materially overstates its trading ML validation, feature engineering, model evaluation, feature importance, and leakage-checking capabilities.

Mitigation: Treat bundled scripts as starting points only; rewrite and test validation, feature engineering, model evaluation, feature importance, and leakage checks before relying on them for trading ML work.

Risk: The security summary flags local file-scanning behavior and deployment utilities with unsafe overwrite and rollback behavior.

Mitigation: Run scripts only on narrow test directories, avoid sensitive workspaces or home directories, and do not use the deployment utility on important targets until overwrite, rollback, and symlink-containment safeguards are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahuserious/skills/ml-pipeline)
- [References README](references/README.md)
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [SHAP Documentation](https://shap.readthedocs.io/)
- [PyTorch Lightning Documentation](https://lightning.ai/docs/pytorch/stable/)
- [Stable-Baselines3 Documentation](https://stable-baselines3.readthedocs.io/)
- [FinRL Repository](https://github.com/AI4Finance-Foundation/FinRL)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks and optional generated files or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce repo-ready pipeline code, configuration templates, validation reports, and deployment commands depending on task.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
