## Description: <br>
Configure Chinese fonts for matplotlib plotting. Use when plotting charts with Chinese characters or getting garbled text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tazio7](https://clawhub.ai/user/Tazio7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Matplotlib for Chinese chart titles, labels, legends, and text annotations, and to troubleshoot garbled Chinese characters or incorrect minus-sign rendering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cache-clearing step deletes local Matplotlib cache files. <br>
Mitigation: Use font listing or font testing first when diagnosing display issues, and run cache clearing only when cache rebuild is intended. <br>


## Reference(s): <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend helper scripts that inspect fonts, test font rendering, or clear the local Matplotlib font cache.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
