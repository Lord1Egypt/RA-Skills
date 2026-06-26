## Description: <br>
Operate Figma through an OOMOL-connected account for reading, creating, updating, and deleting Figma data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect Figma files, metadata, comments, libraries, rendered images, projects, and team resources, and to perform approved Figma write actions through the OOMOL connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a connected Figma account or workspace through OOMOL. <br>
Mitigation: Install only if you trust OOMOL with the connected Figma account and review the requested Figma action before execution. <br>
Risk: Write and destructive actions can change or delete Figma comments, reactions, or dev resources. <br>
Mitigation: Confirm the exact payload and target with the user before write actions, and require explicit approval before destructive actions. <br>
Risk: First-time setup may install the oo CLI or require account connection. <br>
Mitigation: Run setup only after an auth, connection, or missing-command failure and use the documented OOMOL setup flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-figma) <br>
- [Figma homepage](https://www.figma.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, guidance, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses include data and a meta.executionId when actions run with --json.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence release version and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
