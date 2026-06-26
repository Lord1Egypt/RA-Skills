## Description: <br>
Operate Obsidian vaults from the command line for listing, searching, creating, reading, editing, deleting, and managing daily notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[547895019](https://clawhub.ai/user/547895019) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and note-taking users use this skill to operate Obsidian vaults through command-line workflows for note discovery, creation, editing, deletion, and daily-note management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is marked suspicious because it is incomplete and tries to install a missing helper command. <br>
Mitigation: Review the package before installing and confirm the expected helper command is included and executable. <br>
Risk: The installer may make persistent shell changes. <br>
Mitigation: Require explicit user confirmation before modifying shell startup files such as ~/.bashrc. <br>
Risk: The skill advertises editing and deleting private notes. <br>
Mitigation: Require confirmation before destructive note actions and document backup or trash behavior before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/547895019/obsidian-helper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Obsidian helper command and an OBSIDIAN_VAULT path; edit and delete workflows can change vault files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
