## Description: <br>
Manage Obsidian vaults through LiveSync CouchDB by capturing notes, optionally enriching and filing them with AI, managing tasks, and auditing or tidying vault structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[philmossman](https://clawhub.ai/user/philmossman) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Obsidian users use this skill to operate an Obsidian vault through CouchDB/LiveSync, including capture, task management, vault audits, tidying, and AI-assisted note processing or filing when an AI provider is configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool needs direct read/write access to an Obsidian LiveSync CouchDB vault with E2EE disabled. <br>
Mitigation: Use it only with vaults where this access is acceptable, prefer least-privileged CouchDB credentials, and test mutating workflows with dry-run commands first. <br>
Risk: Optional cloud AI providers may process sensitive note content outside the local environment. <br>
Mitigation: Use local Ollama or no-AI mode for sensitive notes, and configure cloud providers only for content that may be sent to that provider. <br>
Risk: Vault credentials are stored in a local configuration file. <br>
Mitigation: Protect the local config file and avoid sharing or checking in `~/.obsidian-curator/config.json`. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/philmossman/obsidian-curator) <br>
- [Obsidian LiveSync](https://github.com/vrtmrz/obsidian-livesync) <br>
- [obsidian-curator project repository listed by skill documentation](https://github.com/philmossman/obsidian-curator) <br>
- [obsidian-curator npm package](https://www.npmjs.com/package/obsidian-curator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include vault-management commands, configuration guidance, markdown task summaries, and API usage examples.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
