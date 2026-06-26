## Description: <br>
PAO System is a personal AI operator framework for skill management, protocol handling, WebSocket communication, cross-device memory sync, and task automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hansondong](https://clawhub.ai/user/hansondong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use PAO System to coordinate AI assistants across devices, share local memory, manage skills, and distribute tasks across networked agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Network task and discovery features can expose listeners or device information beyond intended trusted devices. <br>
Mitigation: Bind listeners to localhost or trusted interfaces, add authentication, and avoid running discovery or task listeners on untrusted LANs. <br>
Risk: Cross-device sync and memory sharing may store or expose local user data under PAO-managed storage. <br>
Mitigation: Review data stored under ~/.pao and disable discovery, sync, or memory sharing unless those features are needed. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/hansondong/pao-system) <br>
- [PAO User Guide](docs/user_guide.md) <br>
- [PAO API Reference](docs/api_reference.md) <br>
- [Task Deployment Guide](task_deploy_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local networking, listener, discovery, sync, and service configuration guidance.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata, SKILL.md frontmatter, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
