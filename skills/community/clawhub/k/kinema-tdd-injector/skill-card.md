## Description: <br>
Generates or updates a repository CLAUDE.md file that injects Kinema's TDD methodology, test structure, coverage gates, network and IO boundaries, fixture rules, and related development conventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeshunee](https://clawhub.ai/user/leeshunee) <br>

### License/Terms of Use: <br>
GNU General Public License v3.0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to initialize or upgrade repository-level TDD guidance in CLAUDE.md for supported Python and TypeScript/JavaScript projects. It is intended as a one-time repository instruction injector before normal development work, with an upgrade path for previously injected repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change repository-level agent instructions in CLAUDE.md. <br>
Mitigation: Review the generated CLAUDE.md diff before accepting changes, especially testing rules, automatic behavior, and enforcement guidance. <br>
Risk: Optional workflows may change project structure or code through paths such as test directory moves or custom config.py generation. <br>
Mitigation: Avoid git mv and custom configuration-generation paths unless those repository mutations are explicitly intended and reviewed. <br>
Risk: Generated guidance may introduce testing, coverage, dependency, or commit conventions that conflict with existing project practices. <br>
Mitigation: Use the documented conflict review path for existing CLAUDE.md content and confirm repository owners accept the resulting conventions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leeshunee/kinema-tdd-injector) <br>
- [README](README.md) <br>
- [Onboarding guide](references/ONBOARDING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and repository file changes, with shell commands and configuration parameters used during generation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent CLAUDE.md guidance and temporary render inputs that should be cleaned up after execution.] <br>

## Skill Version(s): <br>
1.4.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
