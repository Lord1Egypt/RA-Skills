## Description: <br>
Create and manage skill packages by bundling related skills into a single top-level skill with internal dispatch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiguozhi123456](https://clawhub.ai/user/aiguozhi123456) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to consolidate related skills into package skills, refresh package registries, and move sub-skills in or out of packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package creation and add operations remove original top-level skill folders after copying them into a package. <br>
Mitigation: Back up the skills directory first, run commands manually with exact package and skill names, and verify copied package contents before relying on the packaged version. <br>
Risk: A refreshed package registry can misrepresent available sub-skills if source skill frontmatter is stale or incomplete. <br>
Mitigation: Review the generated pack.md and package SKILL.md after each create, add, remove, or update operation. <br>


## Reference(s): <br>
- [ClawHub Package Skill Release Page](https://clawhub.ai/aiguozhi123456/package-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python CLI commands and generated skill package files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates SKILL.md and pack.md files and copies or moves skill directories when its scripts are run.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
