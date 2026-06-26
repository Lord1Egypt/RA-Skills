## Description: <br>
This skill enables one-click generation of multiple AI agents based on a user prompt, outputs their organizational structure, and visualizes their collaboration status using diagrams like swimlane charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brandon-zhanghaodong](https://clawhub.ai/user/brandon-zhanghaodong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to prototype multi-agent systems from natural language prompts, generate role configurations, and create organizational and collaboration diagrams for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The orchestration script writes fixed diagram filenames in the chosen output directory. <br>
Mitigation: Run the skill in a dedicated output directory where overwriting org_chart.* and swimlane.* is acceptable. <br>
Risk: The workflow renders diagrams through a local manus-render-diagram binary. <br>
Mitigation: Use a trusted renderer binary and review local helper scripts before execution. <br>
Risk: Direct script execution uses built-in example prompts instead of the documented CLI flags. <br>
Mitigation: Call the Python functions intentionally or adapt the script interface before relying on documented command-line arguments. <br>


## Reference(s): <br>
- [Reference Documentation for Multi Agent Orchestrator](references/api_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, shell commands] <br>
**Output Format:** [Python-generated agent data, Mermaid diagram code, and PNG diagram files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes org_chart.mmd, org_chart.png, swimlane.mmd, and swimlane.png to the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
