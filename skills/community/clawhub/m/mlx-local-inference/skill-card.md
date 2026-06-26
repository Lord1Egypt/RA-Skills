## Description: <br>
Use this skill to call local AI on an Apple Silicon Mac for text generation, embeddings, speech-to-text, OCR, and image understanding through a local oMLX gateway and MLX Python libraries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bendusy](https://clawhub.ai/user/bendusy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route agent inference tasks to local MLX-based models on Apple Silicon for privacy-sensitive or low-latency workflows. It provides commands and code examples for local chat, vision-language inference, embeddings, speech-to-text, OCR, and oMLX service management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a curl-to-shell command for installing uv. <br>
Mitigation: Review the installer before execution and use an approved package-management path when required by local policy. <br>
Risk: OCR and speech-to-text examples process user-selected local files. <br>
Mitigation: Run the examples only on files intended for local processing and confirm the chosen model paths and output directories before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bendusy/mlx-local-inference) <br>
- [uv installer](https://astral.sh/uv/install.sh) <br>
- [Local oMLX API endpoint](http://localhost:8000/v1) <br>
- [Local oMLX models endpoint](http://localhost:8000/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are local-agent guidance and executable examples; the skill itself does not produce model inference results unless the user runs the referenced local commands.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
