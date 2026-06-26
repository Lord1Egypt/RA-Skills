## Description: <br>
模型蒸馏大师 provides a workflow for transferring capabilities from large teacher models into smaller student models, including teacher analysis, data synthesis, QLoRA training, evaluation, and deployment packaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shixiangyu2](https://clawhub.ai/user/shixiangyu2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML engineers use this skill to plan and execute model distillation workflows for reasoning, math, code, or task-specific model compression. It helps generate training configurations, scripts, evaluation reports, and deployment artifacts for smaller student models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install software, download large models, run model-supplied code, and launch training or deployment scripts. <br>
Mitigation: Use it in a controlled ML environment such as a container or disposable project directory, and review pip, apt-get, brew, git-lfs, git clone, model download, training, and deployment steps before execution. <br>
Risk: Teacher-model API calls and generated training data may expose sensitive or regulated data to external providers. <br>
Mitigation: Avoid sensitive or regulated data unless the teacher provider and its retention policy have been approved. <br>
Risk: Model repositories or generated workflows may rely on remote code execution behavior. <br>
Mitigation: Disable or restrict trust_remote_code unless the model repository is pinned and trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shixiangyu2/model-distill-master) <br>
- [Distillation methodology](references/methodology.md) <br>
- [ModelScope gemma-3-4b-it repository](https://www.modelscope.cn/LLM-Research/gemma-3-4b-it.git) <br>
- [Knowledge distillation paper](https://arxiv.org/abs/1503.02531) <br>
- [DistilBERT paper](https://arxiv.org/abs/1910.01108) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, YAML configuration, Python scripts, JSONL data expectations, and evaluation report descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local training, evaluation, model download, and deployment packaging files when the user approves execution steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact skill.yaml, CHANGELOG dated 2024-04-13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
