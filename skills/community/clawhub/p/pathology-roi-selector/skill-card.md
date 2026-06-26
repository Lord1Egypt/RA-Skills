## Description: <br>
Pathology ROI Selector guides an agent through structured whole-slide-image ROI selection workflows and includes a local Python script that emits reviewable ROI-coordinate output. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, pathology researchers, and educators can use this skill to structure ROI-selection workflows and generate reviewable example ROI JSON from supplied WSI paths. The included script currently returns mock coordinates, so outputs should not be used for clinical, research, or training-data decisions until real image analysis is implemented and reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mock ROI results may be mistaken for real pathology analysis. <br>
Mitigation: Treat the packaged script output as demonstration data only; replace the placeholder implementation with reviewed image analysis before using results for clinical, research, or training-data decisions. <br>
Risk: The local script reads a user-supplied image path and can write an output JSON file. <br>
Mitigation: Run the skill in a sandbox, validate input and output paths, and restrict generated files to the workspace. <br>
Risk: Out-of-scope or incomplete pathology requests can introduce unsupported assumptions. <br>
Mitigation: Confirm required inputs, ROI type, scope limits, and acceptance criteria before execution; stop and request missing inputs when they are not available. <br>


## Reference(s): <br>
- [Pathology ROI Selector ClawHub release](https://clawhub.ai/aipoch-ai/pathology-roi-selector) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; optional JSON ROI-coordinate output from the packaged script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The packaged script accepts an image path, ROI type, and optional output path; current ROI coordinates are mock values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
