## Description: <br>
Helps agents generate and convert PyTorch code for Moore Threads MUSA GPUs using torch_musa. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lipeidcc](https://clawhub.ai/user/lipeidcc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate MUSA-compatible PyTorch patterns, convert CUDA-oriented code to torch_musa conventions, and reason about MUSA environment setup. Review generated code and setup commands before running them in a GPU environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Published metadata describes an OpenAI transcription skill and requests OPENAI_API_KEY, which does not match the MUSA coding helper behavior. <br>
Mitigation: Install only for MUSA and torch_musa coding workflows, and do not provide OPENAI_API_KEY unless the publisher corrects or clearly justifies that requirement. <br>
Risk: Generated CUDA-to-MUSA conversions can change device and distributed backend behavior or write modified Python files. <br>
Mitigation: Review conversion diffs, prefer dry-run review where available, and test converted code in a controlled MUSA environment before relying on it. <br>
Risk: Some setup guidance includes privileged or environment-wide GPU configuration commands. <br>
Mitigation: Run privileged setup only with administrator approval and verify commands against the target MUSA driver, SDK, and conda environment. <br>


## Reference(s): <br>
- [MUSA torch_musa reference](references/reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/lipeidcc/musa-torch-coding) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; the bundled converter can write converted Python files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated conversions and environment commands should be reviewed and tested before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
