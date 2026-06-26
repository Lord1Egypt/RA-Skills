## Description: <br>
Interact with Obsidian vaults through the Obsidian CLI to read, create, search, and manage notes, tasks, properties, and plugin or theme development workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoyaryyj](https://clawhub.ai/user/hoyaryyj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to help Obsidian users work with vault content from the command line. Developers can also use it to support Obsidian plugin and theme reload, inspection, screenshot, console, and JavaScript evaluation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read or modify private Obsidian notes. <br>
Mitigation: Scope commands to named vaults and target files, review mutations before execution, and avoid exposing sensitive note content. <br>
Risk: Developer commands can run JavaScript or use debugging interfaces in Obsidian. <br>
Mitigation: Reserve eval, CDP, and debugger commands for explicit plugin or theme development tasks in trusted vaults. <br>
Risk: The --copy option can place sensitive note content on the system clipboard. <br>
Mitigation: Avoid --copy for private content unless clipboard output is explicitly needed. <br>


## Reference(s): <br>
- [Obsidian CLI documentation](https://help.obsidian.md/cli) <br>
- [ClawHub release page](https://clawhub.ai/hoyaryyj/kepano-obsidian-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include vault, file, path, query, note content, and developer-command arguments for the Obsidian CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
