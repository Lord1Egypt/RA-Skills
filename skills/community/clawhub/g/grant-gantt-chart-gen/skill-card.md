## Description: <br>
Create project timeline visualizations for grant proposals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Grant writers, program managers, and research teams use this skill to generate grant project timelines, milestone summaries, quarterly breakdowns, and text-based chart outputs from milestone data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation describes CSV input and image outputs that the current script does not implement. <br>
Mitigation: Treat the skill as a JSON-to-text timeline generator unless the implementation is extended and rescanned. <br>
Risk: The script writes to a user-supplied output path. <br>
Mitigation: Use project-local output paths and review existing files before writing outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/grant-gantt-chart-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, files] <br>
**Output Format:** [Plain text ASCII chart, Mermaid Gantt code, or JSON timeline data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads optional milestone JSON input and can write the selected output to a user-provided file path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
