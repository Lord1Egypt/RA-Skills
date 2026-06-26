## Description: <br>
Gitignore Sync updates a repository's .gitignore by combining gitignore.io templates with detected repository context while preserving manual rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nikita-holban](https://clawhub.ai/user/nikita-holban) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create or update a repository .gitignore from requested templates and detected project tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated ignore rules can accidentally hide important files from version control. <br>
Mitigation: Review the generated .gitignore diff before committing changes. <br>
Risk: Using an untrusted template endpoint can introduce unwanted ignore rules. <br>
Mitigation: Use the default gitignore.io endpoint unless a deliberate trust decision has been made for another source. <br>
Risk: Running the updater in the wrong directory can modify an unintended repository. <br>
Mitigation: Run the skill only in the repository intended for update and verify the repo path before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nikita-holban/gitignore-sync) <br>
- [Publisher Profile](https://clawhub.ai/user/nikita-holban) <br>
- [gitignore.io API](https://www.toptal.com/developers/gitignore/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash commands; the bundled script writes .gitignore text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Updates or appends a managed .gitignore block while preserving content outside the managed markers.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
