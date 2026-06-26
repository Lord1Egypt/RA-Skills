## Description: <br>
Obsidian Headless lets an agent manage an Obsidian Markdown vault from a headless, SSH, or non-GUI environment by creating, viewing, searching, listing, appending to daily notes, and deleting notes with confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imakid](https://clawhub.ai/user/imakid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, automation users, and note-taking workflows use this skill to manage Obsidian vault notes from command-line or headless environments without launching the Obsidian desktop app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, create, append, search, and delete Markdown files in the configured Obsidian vault. <br>
Mitigation: Configure the vault path deliberately, keep backups of important notes, and review delete confirmations before approving removal. <br>
Risk: The installer changes local shell convenience setup through aliases or symlinks. <br>
Mitigation: Review install.sh before running it and use direct script invocation if shell integration is not desired. <br>


## Reference(s): <br>
- [Obsidian Headless usage manual](USAGE.md) <br>
- [Obsidian](https://obsidian.md/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Natural-language command guidance, shell command examples, and Markdown note content or search results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operates on Markdown files in the configured local Obsidian vault and may create, append, search, view, list, or delete notes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
