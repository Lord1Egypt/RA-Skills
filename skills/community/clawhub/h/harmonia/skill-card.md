## Description: <br>
Check PyTorch, Transformers, and CUDA compatibility. Detect GPU, driver mismatches, and version conflicts in ML environments. Use when the user sets up ML/AI tools, installs torch or transformers, hits dependency errors, or asks about compatible versions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahmed-eladl](https://clawhub.ai/user/ahmed-eladl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Harmonia to diagnose ML dependency, PyTorch, Transformers, CUDA, GPU driver, and Python compatibility issues and to get compatible package-version guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs a third-party Python CLI. <br>
Mitigation: Install it only in environments where third-party Python packages are allowed and review the package-changing command before approval. <br>
Risk: Diagnostic output may expose detailed local system, GPU, driver, Python, and package information. <br>
Mitigation: Review diagnostic output before sharing it outside the local troubleshooting context. <br>
Risk: Suggested pip install or package-changing commands may alter an ML environment. <br>
Mitigation: Review recommendations and run changes in the intended virtual environment before applying them. <br>


## Reference(s): <br>
- [Harmonia homepage](https://github.com/ahmed-eladl/harmonia) <br>
- [harmonia-ml on PyPI](https://pypi.org/project/harmonia-ml/) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local environment diagnostics, compatibility recommendations, and package installation commands for review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
