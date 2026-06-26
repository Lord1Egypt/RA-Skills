## Description: <br>
GitHub DNS Helper helps diagnose and repair GitHub connectivity issues by checking network access and updating GitHub-related hosts entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Thincher](https://clawhub.ai/user/Thincher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users troubleshooting GitHub access use this skill to check connectivity, fetch GitHub hosts records, update the system hosts file, and flush DNS cache when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Changing /etc/hosts ownership can weaken system file protections. <br>
Mitigation: Avoid permanent ownership changes; perform hosts-file edits as a deliberate administrator action and keep the file root- or administrator-owned afterward. <br>
Risk: Custom hosts URLs can introduce unsafe shell input or untrusted hosts entries. <br>
Mitigation: Use only trusted hosts sources, do not pass untrusted custom URLs, and inspect entries before writing them. <br>
Risk: Writing downloaded hosts entries can misroute GitHub traffic or leave connectivity worse than before. <br>
Mitigation: Keep the generated backup, review the changed hosts block, and restore the backup if connectivity or routing behavior is unexpected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Thincher/github-dns-helper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify the system hosts file and DNS cache when executed.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
