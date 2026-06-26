## Description: <br>
Provide commands for interacting with a local Logseq instance through its Plugin API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juanirm](https://clawhub.ai/user/juanirm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Logseq users use this skill to automate local Logseq graphs, including creating pages, inserting or updating blocks, querying tasks and graph data, and managing notes through the Plugin API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A local bridge for the Logseq Plugin API can expose broad read, write, delete, and Git capabilities against a user's notes graph. <br>
Mitigation: Keep any bridge localhost-only, require an auth token, allowlist only needed methods, review proposed edits, confirm deletes and bulk changes, restrict Git commands, and keep backups or version control enabled. <br>


## Reference(s): <br>
- [Logseq Plugin API Documentation](https://logseq.github.io/plugins/) <br>
- [Logseq Plugin Samples](https://github.com/logseq/logseq-plugin-samples) <br>
- [Logseq Plugin API Reference](references/api-reference.md) <br>
- [Logseq Plugin API Examples](references/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/juanirm/logseq) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with JavaScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing instructions and examples for local Logseq Plugin API automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
