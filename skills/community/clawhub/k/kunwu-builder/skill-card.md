## Description: <br>
Controls Kunwu Builder industrial simulation software through its HTTP API for model management, robot control, logistics equipment, cameras, sensors, scenes, and behavior configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SamWLH](https://clawhub.ai/user/SamWLH) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and simulation engineers use this skill to control a Kunwu Builder test or lab environment, create and arrange simulation models, configure gripper and robot behaviors, query scene state, and run supporting Node.js utilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send unauthenticated HTTP commands to configured or hard-coded Kunwu Builder hosts. <br>
Mitigation: Set and verify KUNWU_API_URL before use, prefer an isolated local or lab instance, and avoid running it against shared or production scenes. <br>
Risk: Included scripts and API helpers can reset scenes, destroy or delete models, export data, change behaviors, and load models from cloud-backed sources. <br>
Mitigation: Review the exact script and endpoint before execution, use disposable test scenes, and confirm destructive operations before allowing an agent to run them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/SamWLH/kunwu-builder) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Quickstart](artifact/QUICKSTART.md) <br>
- [Kunwu Builder API Reference](artifact/api-reference.md) <br>
- [Export and Migration Guide](artifact/EXPORT-GUIDE.md) <br>
- [Industrial Patterns](artifact/INDUSTRIAL-PATTERNS.md) <br>
- [Test Report](artifact/TEST-REPORT.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON request bodies, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing instructions and API call patterns; scripts may send HTTP commands to a configured Kunwu Builder instance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
