## Description: <br>
Build, test, and deploy custom Linux ISOs with OpenFactory. Create VMs, run compliance tests, manage recipes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziegenbalg](https://clawhub.ai/user/ziegenbalg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to build custom Linux ISOs, deploy them into VMs, run compliance-oriented tests, and manage recipes through OpenFactory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create, start, stop, or delete VMs and retrieve ISO download or console URLs. <br>
Mitigation: Require explicit confirmation before destructive VM actions and protect console URLs, session tokens, API keys, and ISO download links. <br>
Risk: Build recipes and git deployment workflows may include untrusted repositories, weak example passwords, or unrelated secrets. <br>
Mitigation: Use trusted repositories, replace example passwords, validate recipes before builds, and avoid placing unrelated secrets in recipes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ziegenbalg/openfactory) <br>
- [OpenFactory homepage](https://openfactory.tech) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON examples and tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include build recipes, VM and test workflow steps, API authentication guidance, and ISO download or console handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
