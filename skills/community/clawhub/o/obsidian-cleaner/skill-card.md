## Description: <br>
Automatically clean up loose images and attachments in Obsidian vault root, moving them to the Attachments folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sparkingskin-tech](https://clawhub.ai/user/sparkingskin-tech) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Obsidian users use this skill to find loose files in an Obsidian vault root and move them into an Attachments folder. It is intended for local vault organization with a dry-run option before changes are made. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cleanup script can move root-level .md and .txt files as well as image and document attachments. <br>
Mitigation: Run the dry-run command first, review every proposed move, and remove .md or .txt from the extension list before live cleanup if notes or text files should remain in the vault root. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sparkingskin-tech/obsidian-cleaner) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script reports found, moved, skipped, and errored files; dry-run output previews moves without changing files.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, _meta.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
