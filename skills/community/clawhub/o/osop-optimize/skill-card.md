## Description: <br>
Analyze .osoplog execution history to optimize workflows by finding slow steps and parallelization opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archie0125](https://clawhub.ai/user/archie0125) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow maintainers use this skill to inspect OSOP workflow execution logs, identify slow or unreliable nodes, and propose workflow improvements. With user approval, it can apply changes to the selected .osop workflow after showing a diff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow edits could change production behavior or introduce incorrect optimization guidance. <br>
Mitigation: Review the proposed diff before approving any write, especially for production workflows. <br>
Risk: Execution logs may contain sensitive operational details. <br>
Mitigation: Limit log access to the intended workflow context and avoid sharing log-derived findings outside authorized channels. <br>


## Reference(s): <br>
- [OSOP homepage](https://osop.ai) <br>
- [ClawHub release page](https://clawhub.ai/archie0125/osop-optimize) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown analysis with suggestion tables, diffs, and optional workflow file edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a target .osop workflow path and may read matching .osoplog.yaml files from sessions/ or the workflow directory.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
