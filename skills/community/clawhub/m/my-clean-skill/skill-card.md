## Description: <br>
A skill that enables AI agents to create and verify decentralized identities using Billions Network. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[gamingjancok11-ctrl](https://clawhub.ai/user/gamingjancok11-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent builders use this skill to guide agents through creating and verifying decentralized identities, linking agent and human identities, and interacting with decentralized identity systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security guidance notes that some bundled workflows can change public or account state. <br>
Mitigation: Review moderation-related actions before use and limit execution to expected ClawHub or Convex development environments. <br>
Risk: The security guidance notes that autoreview may default to a full-access nested review. <br>
Mitigation: Run autoreview with --no-yolo or AUTOREVIEW_YOLO=0 when full-access nested review is not intended. <br>
Risk: The skill requires Billions Network access, so identity operations may depend on external network availability and credentials. <br>
Mitigation: Confirm the target environment has the required Node.js setup and Billions Network access before relying on the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gamingjancok11-ctrl/my-clean-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown guidance for agent workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Node.js environment and Billions Network access when following the skill guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
