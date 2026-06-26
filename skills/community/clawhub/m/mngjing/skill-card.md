## Description: <br>
Offline, zero-dependency health monitoring for LLM agents with multi-framework support and a web dashboard for real-time diagnostics and grading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wulun811](https://clawhub.ai/user/wulun811) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and operate Mingjing for local health monitoring, diagnostics, and grading of LLM agent systems across supported frameworks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow installs external packages and an OpenClaw plugin. <br>
Mitigation: Verify the `mingjing` package and `mingjing-probe` plugin provenance before installation. <br>
Risk: The workflow starts a local daemon and web dashboard. <br>
Mitigation: Confirm what telemetry is stored locally and stop the daemon and dashboard when they are not in use. <br>


## Reference(s): <br>
- [Mingjing ClawHub Page](https://clawhub.ai/wulun811/mngjing) <br>
- [Mingjing GitHub Repository](https://github.com/wulun811/Ming_qiankun) <br>
- [Mingjing GitHub Issues](https://github.com/wulun811/Ming_qiankun/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with bash code blocks and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation steps, feature summaries, diagnostic coverage, and local dashboard instructions.] <br>

## Skill Version(s): <br>
0.11.14 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
