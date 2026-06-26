## Description: <br>
End-to-end LoRA training pipeline for collecting reference photos, verifying faces, scraping image datasets, applying quality checks, captioning with WD14, and training on RunPod. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iskWang](https://clawhub.ai/user/iskWang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to prepare face-image datasets, caption them, and train LoRA model outputs through a staged workflow. It is suited for agent-assisted dataset preparation and training orchestration when the user has rights and consent for the images involved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow handles face-image datasets that may include personal or sensitive images. <br>
Mitigation: Confirm rights and consent for all images before collection, verification, captioning, or training. <br>
Risk: The workflow references login-bypassing mirror sites for image scraping. <br>
Mitigation: Avoid login-bypassing sources and use only permitted, rights-cleared image sources. <br>
Risk: The workflow uploads training data to RunPod for remote training. <br>
Mitigation: Use the workflow only when cloud processing is acceptable, verify RunPod account and cost settings, and manually confirm remote datasets and pods are deleted after training. <br>
Risk: ZIP extraction and captioning can overwrite or alter local dataset files. <br>
Mitigation: Review ZIP contents before extraction and back up existing captions or datasets before running captioning and training steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iskWang/lora-pipeline) <br>
- [Publisher profile](https://clawhub.ai/user/iskWang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces phase status messages, dataset paths, training commands, configuration defaults, and local LoRA output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
