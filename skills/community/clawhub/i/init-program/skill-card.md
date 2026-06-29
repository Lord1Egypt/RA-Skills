## Description: <br>
Create or update the correct agent instruction file for the active coding assistant, then initialize a software project according to that file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dreamingphper](https://clawhub.ai/user/dreamingphper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent users use this skill to establish the right repository instruction file, then bootstrap or update project structure, setup commands, validation expectations, and code review rules from that instruction contract. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update agent instruction files and scaffold project files, which may change how future agents work in the repository. <br>
Mitigation: Review the selected assistant file, instruction language, generated files, and project structure before accepting changes in an important repository. <br>
Risk: Initialization may involve dependency, generator, setup, or validation commands that affect the workspace. <br>
Mitigation: Confirm the technology stack and review proposed commands before allowing them to run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dreamingphper/init-program) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with proposed file edits and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update AGENTS.md or CLAUDE.md and scaffold minimal project files after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
