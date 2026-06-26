## Description: <br>
Connect OpenClaw to the claw-school training flow with an enrollment code, use default training URLs unless overridden, ensure clawhub is available, install the mapped ClawHub skills for that package, and report each training step back to the claw-school server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darrenluo](https://clawhub.ai/user/darrenluo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to complete a real claw-school enrollment, run each required training phase, install the server-mapped ClawHub skills for the course package, and report progress back to the web app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install server-selected ClawHub skills and change the user's environment. <br>
Mitigation: Use it only with a trusted training server and registry, review the exact skills and commands before installation, and prefer dry-run behavior first. <br>
Risk: The skill reports training progress and the current workspace path to the training server. <br>
Mitigation: Run it from a non-sensitive workspace and confirm the intended enrollment server before starting. <br>
Risk: Training results may be misleading because assessment scores are generated locally by the artifact. <br>
Mitigation: Treat the scores as course progress signals, not as an independent capability evaluation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/darrenluo/openclaw-school-enrollment) <br>
- [OpenClaw School training server](https://openclaw-school.space) <br>
- [ClawHub mirror registry](https://cn.clawhub-mirror.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured JSON from the enrollment script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces short user-facing progress updates and may run installation commands unless dry-run behavior is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
