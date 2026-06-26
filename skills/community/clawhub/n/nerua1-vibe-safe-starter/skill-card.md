## Description: <br>
Provides a minimal security starter pack that helps developers add dependency audits, package checks, and basic secret scanning to AI-generated projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nerua1](https://clawhub.ai/user/nerua1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add a small security baseline to vibe-coded repositories, including npm and Python dependency checks, package vetting, and simple secret scanning before install or deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included checks are lightweight and may miss vulnerabilities, malicious packages, or secrets that require deeper review. <br>
Mitigation: Treat clean results as a first-pass signal, then use maintained security tools and human review before production deployment. <br>
Risk: The shell scripts inspect local project files and query external package and vulnerability registries. <br>
Mitigation: Review the scripts before running them, use trusted workspaces, and avoid exposing sensitive project details where that is not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nerua1/nerua1-vibe-safe-starter) <br>
- [Publisher profile](https://clawhub.ai/user/nerua1) <br>
- [VibeSafe Extension](https://github.com/nerua1/vibe-safe) <br>
- [VibeSafe full audit pipeline](https://github.com/nerua1/vibe-safe) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash commands and configuration file instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct users to run local shell scripts and review dependency, registry, vulnerability, and secret-scan results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
