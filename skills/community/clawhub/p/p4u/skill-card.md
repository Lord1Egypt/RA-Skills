## Description: <br>
Perforce / Helix Core (p4) power-user CLI for inspecting and managing changelists, shelves, workspaces, file annotations, syncs, and depot workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m9rco](https://clawhub.ai/user/m9rco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run common Perforce and Helix Core workflows through the p4u CLI, including changelist inspection, shelving, switching, annotation, syncing, cleanup, and untracked-file discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Powerful Perforce operations can change or remove workspace, changelist, or shelved data. <br>
Mitigation: Review the active user, client, and command before approval, especially delete, revert, sync, switch, or force operations. <br>
Risk: The p4u binary and the Perforce environment are external prerequisites. <br>
Mitigation: Install only if the p4u release source and the target Perforce environment are trusted. <br>


## Reference(s): <br>
- [p4u ClawHub page](https://clawhub.ai/m9rco/p4u) <br>
- [p4u source repository](https://github.com/m9rco/p4u-skill) <br>
- [p4u releases](https://github.com/m9rco/p4u-skill/releases) <br>
- [Perforce Helix Command-Line Client](https://www.perforce.com/downloads/helix-command-line-client-p4) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should use --non-interactive; destructive Perforce operations require explicit user confirmation.] <br>

## Skill Version(s): <br>
0.0.0-nightly.e055304 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
