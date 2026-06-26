## Description: <br>
Sync and manage Overleaf LaTeX projects from the command line, including pulling projects locally, pushing changes, compiling PDFs, and downloading compile outputs like .bbl files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aloth](https://clawhub.ai/user/aloth) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, researchers, and technical writers use this skill to manage Overleaf LaTeX projects from the command line, including authentication, synchronization, compilation, and export workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a live Overleaf session cookie and may store it in environment variables, a local `.olauth` file, or global config. <br>
Mitigation: Avoid shell history, shared terminals, screenshots, project folders, and source control; protect `.olauth` and config files; refresh the cookie if exposure is suspected. <br>
Risk: Push, sync, and force overwrite workflows can change or overwrite project files. <br>
Mitigation: Use dry runs, backups, and status checks before `push`, `sync`, or forced overwrite commands. <br>
Risk: The workflow installs and uses the external `olcli` package. <br>
Mitigation: Review the package source and installer path before installing through Homebrew or npm. <br>


## Reference(s): <br>
- [Overleaf API Reference](references/API.md) <br>
- [olcli GitHub repository](https://github.com/aloth/olcli) <br>
- [olcli npm package](https://www.npmjs.com/package/@aloth/olcli) <br>
- [Overleaf](https://www.overleaf.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes install, authentication, synchronization, compilation, export, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
