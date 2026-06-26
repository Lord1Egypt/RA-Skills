## Description: <br>
Native Linear lets agents query and manage Linear issues, projects, cycles, teams, and workflow states directly through the Linear GraphQL API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeninja23](https://clawhub.ai/user/codeninja23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workflow agents use this skill to inspect Linear teams, issues, projects, cycles, and states, and to create or update issues from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Linear API key that may grant access to workspace issue data. <br>
Mitigation: Use a least-privileged Linear API key where possible and install the skill only for workspaces where agent access is acceptable. <br>
Risk: Create and update commands can change Linear issues in an important workspace. <br>
Mitigation: Review proposed create or update actions before allowing an agent to run them. <br>


## Reference(s): <br>
- [Native Linear on ClawHub](https://clawhub.ai/codeninja23/native-linear) <br>
- [Linear GraphQL API](https://api.linear.app/graphql) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text terminal output with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and LINEAR_API_KEY; create and update commands can modify Linear workspace issues.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
