## Description: <br>
Reply cites file paths, directories, or module locations that do not exist in the current project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mvogt99](https://clawhub.ai/user/mvogt99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to identify and avoid responses that cite invented file paths, directories, or module locations. It supports safer repo work by prompting filesystem checks before quoting, editing, or creating paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill addresses cases where an agent may cite or act on file paths that do not exist. <br>
Mitigation: Verify paths with filesystem checks such as ls, stat, or repository search before quoting, editing, or creating files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mvogt99/hallucinated-paths) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mvogt99) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
