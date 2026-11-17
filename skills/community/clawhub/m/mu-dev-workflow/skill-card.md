## Description:

A Markdown workflow skill that guides AI agents through requirements clarification, design self-checks, planned execution, sub-agent review, and command-backed verification for code and skill-development work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muippt](https://clawhub.ai/user/muippt)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to slow down coding and skill-authoring requests until requirements, design choices, execution plans, and verification evidence are explicit. It is most relevant for feature work, bug fixes, refactors, new skills, and proposal review workflows where premature implementation is a risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly control development behavior by imposing hard gates across coding, refactoring, bug fixing, and skill-authoring requests.

Mitigation: Install it only where that workflow control is intended, and prefer explicit invocation or narrowly scoped activation for repositories that do not need strict process gates.

Risk: Persistent instruction changes could make the workflow difficult to bypass or audit if copied into global agent instruction files.

Mitigation: Keep the skill in a reviewable project or skill directory, avoid writing its rules into global instruction files, and review changes before making them persistent.

Risk: The artifact references external skills and audit scripts that are not bundled as executable evidence in this release.

Mitigation: Verify any external skill or audit script before use and do not treat referenced tools as trusted solely because this workflow mentions them.

## Reference(s):

- [Architecture Pattern Library](references/architecture-patterns.md)
- [Anti-rationalization Table](references/anti-rationalization.md)
- [Sub-agent Review Templates](references/subagent-review-templates.md)
- [Superpowers](https://github.com/obra/superpowers)
- [ClawHub Skill Page](https://clawhub.ai/muippt/skills/mu-dev-workflow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured checklists, design notes, task plans, review prompts, code changes, and verification command output when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pure Markdown workflow; no runtime dependencies or credential inputs are described in the artifact.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter and changelog report 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
