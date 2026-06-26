## Description: <br>
ML Pipeline guides agents through quantitative trading ML workflows, including feature engineering, AutoML, deep learning, financial RL, model training, and anti-leakage validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahuserious](https://clawhub.ai/user/ahuserious) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and quantitative research teams use this skill to plan, implement, validate, and deploy machine learning pipelines for trading research. It is most useful for feature engineering, automated model search, model evaluation, and leakage-aware time-series validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill overstates its ML and trading capabilities. <br>
Mitigation: Treat generated trading pipeline guidance as a starter template and validate all claims, metrics, and model choices against your own data and review process. <br>
Risk: The security review notes broad local command and file authority, including scripts that can scan, copy, overwrite, and delete files. <br>
Mitigation: Install only in a dedicated workspace, inspect proposed Bash, Write, and Edit actions before approving them, and use deployment helpers only with source and target paths you are comfortable modifying. <br>
Risk: Recursive analyzers and bundled utility scripts may traverse sensitive directories if pointed at broad paths. <br>
Mitigation: Run scripts only on scoped project directories or sanitized sample data, and avoid using sensitive home, credential, or production directories as inputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ahuserious/ml-pipeline) <br>
- [References README](references/README.md) <br>
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) <br>
- [SHAP Documentation](https://shap.readthedocs.io/) <br>
- [PyTorch Lightning Documentation](https://lightning.ai/docs/pytorch/stable/) <br>
- [Stable-Baselines3 Documentation](https://stable-baselines3.readthedocs.io/) <br>
- [FinRL](https://github.com/AI4Finance-Foundation/FinRL) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, configuration examples, and repo-ready file changes when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or modify local scripts, configuration files, reports, and deployment artifacts.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
