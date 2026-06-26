## Description: <br>
Generates .gitignore files from GitHub's official template collection, with support for combining templates, project detection, custom rules, and writing or printing output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate, combine, preview, append, or overwrite .gitignore files for new and existing repositories using GitHub's official templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite or append to .gitignore files when generation flags request file writes. <br>
Mitigation: Preview generated output with --stdout and avoid --force in important repositories unless the changes have been reviewed. <br>
Risk: The skill retrieves template data from GitHub and depends on network availability and upstream template content. <br>
Mitigation: Run it in an environment where GitHub access is expected, and review generated .gitignore content before committing it. <br>


## Reference(s): <br>
- [GitHub gitignore templates API](https://api.github.com/gitignore/templates) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands; generated .gitignore text or files when the script is run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write, append, or print .gitignore content depending on command flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
