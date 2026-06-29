## Description: <br>
Plans, drafts, and refines technical tutorials for developers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to plan, draft, and refine hands-on tutorials with scoped audiences, runnable examples, expected outputs, troubleshooting coverage, and quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and edit repository documentation and agent instruction files, which could introduce inaccurate or unwanted guidance in sensitive repositories. <br>
Mitigation: Use a narrow file scope, request report-only review when edits are not desired, and review proposed documentation changes before accepting them. <br>
Risk: Tutorials produced by the skill may include code examples or shell commands that affect a user's environment. <br>
Mitigation: Require snippets to be tested in a real or isolated environment and verify stated output before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-scribe-tech-tutorial) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scribe) <br>
- [Tutorial outline structure module](artifact/modules/outline-structure.md) <br>
- [Code examples module](artifact/modules/code-examples.md) <br>
- [Progressive complexity module](artifact/modules/progressive-complexity.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with outlines, draft prose, code blocks, command examples, checklists, and review notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to repository documentation and agent instruction files when asked.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
