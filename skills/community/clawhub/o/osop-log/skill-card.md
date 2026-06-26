## Description: <br>
Generates OSOP session logs by creating .osop workflow definitions and .osoplog.yaml execution records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archie0125](https://clawhub.ai/user/archie0125) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill after completing a task to record what happened as a structured workflow and execution log for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated session logs may capture secrets, private project details, command output, or sensitive reasoning. <br>
Mitigation: Review generated .osop and .osoplog.yaml files before committing, sharing, or uploading them to a viewer. <br>


## Reference(s): <br>
- [OSOP](https://osop.ai) <br>
- [OSOP log viewer](https://osop-editor.vercel.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown instructions with YAML file content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local .osop and .osoplog.yaml session records under a sessions directory.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
