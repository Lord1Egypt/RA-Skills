## Description: <br>
Peace Workflow guides an agent through reviewing, improving, versioning, and delivering HTML game or UI files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kukuxNd](https://clawhub.ai/user/kukuxNd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to run a structured review-and-improvement loop for HTML game or UI files, including reviewer feedback analysis, code changes, versioned output, and result delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow asks the agent to send selected local HTML files through Feishu without clear destination checks. <br>
Mitigation: Before execution, confirm the exact local file path, recipient or channel, and output filename. <br>
Risk: HTML files may contain secrets, private data, or confidential project content. <br>
Mitigation: Do not use the workflow on sensitive files unless the user has reviewed the contents and approved sharing through the configured channel. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Markdown] <br>
**Output Format:** [Markdown guidance with HTML code edits and versioned file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a new versioned HTML file, changelog notes, review scores, and delivery instructions when the agent has appropriate tool access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
