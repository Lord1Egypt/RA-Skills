## Description: <br>
Simulate physics experiments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and science users can use this skill to run physics simulation tasks from the command line and receive JSON results for experiments or automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references scripts/physics_simulator.py, but the artifact does not include that executable code. <br>
Mitigation: Verify the simulator script source and behavior before running the command from this skill. <br>
Risk: The skill requires SIMULATION_API_KEY, which could expose credentials if scoped or stored incorrectly. <br>
Mitigation: Confirm the service the key authenticates to, use a minimal-scope key, and avoid storing secrets in shared logs or committed files. <br>


## Reference(s): <br>
- [Physics Simulator ClawHub page](https://clawhub.ai/jpengcheng523-netizen/jpeng-physics-simulator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, configuration instructions, and JSON result expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires users to provide an input path, output path, and SIMULATION_API_KEY for the referenced simulator command.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter, released 2026-03-26) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
