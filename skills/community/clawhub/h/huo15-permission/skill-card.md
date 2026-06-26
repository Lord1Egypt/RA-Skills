## Description: <br>
火一五权限 is a permission-control skill that checks user IDs and restricts create, update, delete, install, and uninstall actions, with ZhaoBo as the hardcoded administrator. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jobzhao15](https://clawhub.ai/user/jobzhao15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Workspace users can use this skill to enforce a simple role boundary for agent actions: ZhaoBo may perform all configured operations, while other users are limited to changes within existing skills and are blocked from installing or uninstalling skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives broad control over agent behavior by attempting to intercept install, uninstall, and editing requests based on a hardcoded administrator. <br>
Mitigation: Install only in workspaces that intentionally delegate those decisions to ZhaoBo, and confirm the configured administrator and default permission level before use. <br>
Risk: Keyword-based permission checks can block legitimate skill management or miss requests phrased outside the configured trigger terms. <br>
Mitigation: Test the configured trigger terms in a controlled workspace and review blocked actions before relying on the skill for operational permission boundaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jobzhao15/huo15-permission) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain-text agent responses with JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Permission decisions depend on message userid metadata and keyword matching configured in config.json.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
