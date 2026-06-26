## Description: <br>
Use when operating Halo themes, plugins, attachments, backups, or moments from the terminal, including install, upgrade, activate, upload, download, create, delete, and batch maintenance flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruibaby](https://clawhub.ai/user/ruibaby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and administrators use this skill to operate Halo sites from the terminal, especially when managing themes, plugins, attachments, backups, and moments. It helps agents propose Halo CLI commands and safety checks for routine and mutating maintenance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mutating Halo operations can affect themes, plugins, attachments, backups, or moments in the selected environment. <br>
Mitigation: Verify the Halo profile, resource name, source URL, and command intent before running mutating actions. <br>
Risk: Force and non-interactive confirmation flags can bypass prompts for destructive or remote-source operations. <br>
Mitigation: Reserve --force and --yes for actions already reviewed by the user or automation owner. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the halo command-line binary and a selected Halo profile for environment-specific operations.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
