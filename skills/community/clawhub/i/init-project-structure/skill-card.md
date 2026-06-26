## Description: <br>
Scaffolds a new project with CLAUDE.md, gitignored local notes, a docs tree, plan and recap directories, contract documents, and housekeeping protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adelvillar1](https://clawhub.ai/user/adelvillar1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when starting a project or adding structured methodology to an existing codebase. It creates project memory, documentation scaffolds, plan and recap folders, and safety checks for local setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated project guidance or contract documents may encode inaccurate assumptions if project facts are incomplete. <br>
Mitigation: Review generated CLAUDE.md, TECHNICAL-DOCUMENTATION.md, and FUNCTIONAL-SPECIFICATIONS.md before relying on them. <br>
Risk: Local environment notes could expose credentials if committed. <br>
Mitigation: Keep CLAUDE.local.md gitignored and use placeholder sections until real credentials are added locally. <br>
Risk: Workflow guidance may include production deploys or destructive cleanup commands. <br>
Mitigation: Check the exact action before approving production changes, destructive operations, or cleanup commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adelvillar1/init-project-structure) <br>
- [CLAUDE template for simple topology](references/CLAUDE-template-simple.md) <br>
- [CLAUDE template for full topology](references/CLAUDE-template-full.md) <br>
- [Technical documentation template](references/TECHNICAL-DOCUMENTATION-template.md) <br>
- [Functional specifications template](references/FUNCTIONAL-SPECIFICATIONS-template.md) <br>
- [Plans README template](references/docs-plans-README-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files, shell command blocks, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project scaffolding files and prompts for project-specific facts before writing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
