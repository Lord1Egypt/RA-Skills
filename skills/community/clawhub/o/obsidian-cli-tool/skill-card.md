## Description: <br>
Interact with Obsidian vaults through the Obsidian CLI to read, create, search, and manage notes, tasks, frontmatter, plugin reloads, JavaScript evaluation, screenshots, errors, and DOM inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sadlay](https://clawhub.ai/user/sadlay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, writers, and knowledge workers use this skill to operate an Obsidian vault from an agent, including note management, vault search, frontmatter updates, and plugin or theme debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live vault operations can delete, move, or change notes and frontmatter. <br>
Mitigation: Ask for confirmation before delete, move, or frontmatter-changing commands. <br>
Risk: Plugin JavaScript evaluation can run code inside Obsidian. <br>
Mitigation: Use plugin evaluation only with code the user trusts and after explicit confirmation. <br>
Risk: Screenshots and DOM inspection can expose vault or workspace information. <br>
Mitigation: Ask for confirmation before screenshots or DOM inspection and avoid exposing sensitive content. <br>
Risk: The workflow depends on a separate Obsidian CLI/plugin and a running Obsidian instance. <br>
Mitigation: Verify the Obsidian CLI/plugin installation and the active Obsidian instance before relying on commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target a running Obsidian instance and require the Obsidian CLI plugin.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
