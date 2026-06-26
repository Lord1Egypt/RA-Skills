## Description: <br>
Run Python code on cloud GPUs using the Modal serverless platform for A100, T4, and A10G GPU access, covering app setup, GPU selection, data downloading inside functions, and result handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to draft and troubleshoot Modal-based Python workflows for remote GPU training, including dependency setup, GPU sizing, data access, execution, and returning results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Modal and HuggingFace tokens can grant access to cloud compute or private data if exposed. <br>
Mitigation: Treat tokens as secrets, use Modal secrets for private HuggingFace access, and avoid exposing credentials in shell history or logs. <br>
Risk: Detached or long-running remote GPU jobs can create unexpected cloud cost. <br>
Mitigation: Review training scripts before execution, set appropriate timeouts, monitor detached jobs, and stop unneeded runs. <br>
Risk: Persistent volumes and downloaded datasets may retain private or sensitive data. <br>
Mitigation: Use persistent volumes intentionally and clean up cached data or volumes that are no longer needed. <br>


## Reference(s): <br>
- [Getting Started with Modal](references/getting-started.md) <br>
- [GPU Selection](references/gpu-selection.md) <br>
- [Data Download in Modal](references/data-download.md) <br>
- [Returning Results from Modal](references/results.md) <br>
- [Common Issues](references/common-issues.md) <br>
- [Modal Documentation](https://modal.com/docs) <br>
- [Modal Examples](https://github.com/modal-labs/modal-examples) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Modal app snippets, GPU recommendations, dependency declarations, token setup commands, and troubleshooting steps.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
