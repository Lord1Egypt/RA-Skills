## Description: <br>
NVIDIA LocateAnything-3B vision-language grounding model that guides agents through inference APIs, data preparation, training, fine-tuning, evaluation, and output parsing for detection, visual grounding, OCR, and GUI recognition. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0; upstream code Apache 2.0; model NVIDIA License (non-commercial research) <br>


## Use Case: <br>
Developers and engineers use this skill to apply LocateAnything-3B for visual grounding workflows, including object detection, point and box grounding, OCR, GUI element recognition, dataset formatting, fine-tuning, and benchmark evaluation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs users to clone and run upstream machine-learning repositories. <br>
Mitigation: Review upstream code and licenses before execution, and run installation, inference, and training in an isolated virtual environment or container. <br>
Risk: The referenced model is described as non-commercial research use. <br>
Mitigation: Confirm model license terms and restrict usage to research and development unless separate commercial rights are verified. <br>
Risk: Guidance includes high-resource training and evaluation commands that may fail or behave differently across GPU generations. <br>
Mitigation: Match attention implementation, sequence length, and token budgets to available hardware, and validate commands on a small dataset before larger runs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/openlark/locateanything) <br>
- [NVIDIA LocateAnything-3B model card](https://huggingface.co/nvidia/LocateAnything-3B) <br>
- [LocateAnything Hugging Face demo](https://huggingface.co/spaces/nvidia/LocateAnything) <br>
- [NVlabs Eagle repository](https://github.com/NVlabs/Eagle) <br>
- [Eagle project page](https://nvlabs.github.io/Eagle/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, shell, JSON, and JSONL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include normalized box or point coordinate formats and benchmark or fine-tuning command examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
