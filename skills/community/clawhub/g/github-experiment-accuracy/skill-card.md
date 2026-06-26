## Description: <br>
Guides an agent through cloning or downloading a GitHub project, running model predictions on a supplied dataset, calculating accuracy metrics, and producing experiment reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevinyyc](https://clawhub.ai/user/kevinyyc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML evaluators use this skill to run a GitHub-hosted model project against a provided dataset, compute MAE, RMSE, MAPE, and accuracy, and generate reproducible experiment reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Loading untrusted PyTorch model files with weights_only=false can execute code from an untrusted repository download. <br>
Mitigation: Use a disposable isolated environment, avoid sensitive files and credentials, prefer safetensors or a verified state_dict, and review repository code and dependencies before evaluation. <br>
Risk: Cloning or downloading arbitrary GitHub projects may expose the agent runtime to untrusted code and dependencies. <br>
Mitigation: Evaluate repositories only in a sandbox with limited network reachability and inspect dependency installation and execution steps before running them. <br>


## Reference(s): <br>
- [GitHub Experiment Accuracy Workflow](artifact/references/workflow.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kevinyyc/github-experiment-accuracy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, code snippets, report templates, and JSON result paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include accuracy_report.md, experiment_report.md, and outputs/daily_results.json in the evaluated project workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
