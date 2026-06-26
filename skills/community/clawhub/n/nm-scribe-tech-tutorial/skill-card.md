## Description: <br>
Plans, drafts, and refines technical tutorials for developers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to plan, draft, and verify getting-started guides, hands-on walkthroughs, and technical tutorials backed by runnable code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit documentation or agent instruction files outside the intended scope. <br>
Mitigation: Name the target files explicitly and request report-only behavior when auditing; review proposed diffs before accepting changes. <br>
Risk: A tutorial can mislead readers if code examples are not tested in the target environment. <br>
Mitigation: Require tested snippets, exact prerequisite versions, expected output blocks, and explicit notes for any untested platform or command. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/nm-scribe-tech-tutorial) <br>
- [Project Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scribe) <br>
- [Writing Effective Code Examples](modules/code-examples.md) <br>
- [Tutorial Outline and Structure](modules/outline-structure.md) <br>
- [Building Complexity Gradually](modules/progressive-complexity.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with fenced code blocks, checklists, outlines, and prose guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tutorial outlines, tested code snippets, expected output blocks, troubleshooting notes, and quality-gate checklist items.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
