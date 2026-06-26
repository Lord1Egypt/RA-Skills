## Description: <br>
Meegle Open API skills index for finding credentials and task-specific Meegle API sub-skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pkycy](https://clawhub.ai/user/pkycy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations teams use this skill pack to guide an agent through authenticated Meegle Open API work for spaces, users, work items, settings, comments, views, and measurements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured Meegle plugin credentials can let an agent read or change project data. <br>
Mitigation: Use a least-privilege Meegle plugin, restrict the configured project and user scope where possible, and require explicit confirmation of target projects, object IDs, names, and intended changes before broad or destructive actions. <br>
Risk: Long-lived Meegle credentials may be stored in the OpenClaw configuration file. <br>
Mitigation: Protect ~/.openclaw/openclaw.json with local file permissions and rotate the plugin secret if that file is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pkycy/meegle-api) <br>
- [README](README.md) <br>
- [Credentials skill](meegle-api-credentials/SKILL.md) <br>
- [Skill index](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, code, shell commands] <br>
**Output Format:** [Markdown guidance with API specs, JSON configuration examples, and request snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured Meegle plugin, domain, project, and user credentials before API guidance can be used.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
