## Description: <br>
API specification management skill for initializing, updating, querying, and searching cross-project API documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexxxiong](https://clawhub.ai/user/alexxxiong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API maintainers use this skill to create local API specification configuration, inspect existing API documentation, search across a shared API registry, and generate updates from backend route definitions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The update workflow can commit and push generated API documentation to a Git repository. <br>
Mitigation: Review the configured repository, target branch, and generated diff before allowing publication. <br>
Risk: Generated API documentation may expose internal endpoints or sensitive request and response fields. <br>
Mitigation: Exclude sensitive routes and fields before syncing or publishing the API registry. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexxxiong/inspirai-apispec) <br>
- [Publisher profile](https://clawhub.ai/user/alexxxiong) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with shell commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or generate .api-spec.yaml configuration and API documentation YAML files for a user-controlled registry.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
