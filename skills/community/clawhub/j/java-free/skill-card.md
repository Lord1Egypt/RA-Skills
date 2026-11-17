## Description: <br>
Java基础版 helps agents review and generate basic Java code focused on null safety, equals/hashCode, try-with-resources, collections, and exception handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code reviewers use this skill to inspect Java snippets or files for common robustness issues and to receive fix guidance or simple generated implementations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill declares write and exec capabilities, so an agent may edit project files or run Java-related commands when allowed. <br>
Mitigation: Use it in trusted projects, review proposed edits and commands before execution, and keep agent permissions scoped to the intended Java files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/java-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown, JSON, or text with Java code snippets and review findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include issue summaries, scores, prioritized improvements, rewritten Java snippets, and execution logs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
