## Description: <br>
Converts Kindle HTML notebook exports into Obsidian-ready Markdown notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[henrCh1](https://clawhub.ai/user/henrCh1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert a Kindle notes HTML export into a Markdown file for an Obsidian books folder after configuring the output directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite an existing Markdown note with the same generated filename. <br>
Mitigation: Confirm the generated book title and output path before running it; keep backups or remove override behavior when replacement is not intended. <br>
Risk: The output directory starts as a placeholder configuration value. <br>
Mitigation: Set references/config.md to the exact intended Obsidian folder before using the conversion command. <br>
Risk: The conversion script depends on Python packages installed in the local environment. <br>
Mitigation: Install required Python packages only from trusted package sources. <br>


## Reference(s): <br>
- [Configuration reference](references/config.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown file plus concise user-facing status or error text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a configured output directory, derives the output filename from the Kindle export filename, and may overwrite an existing Markdown file when run with override behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
