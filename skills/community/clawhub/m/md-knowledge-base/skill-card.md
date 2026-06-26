## Description: <br>
Knowledge-Base guides an agent through creating, organizing, searching, archiving, and health-checking a structured Markdown knowledge base using configurable reference rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[otweihan](https://clawhub.ai/user/otweihan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and agent operators use this skill to maintain a Markdown knowledge base: add notes, organize projects, record daily or weekly updates, capture external sources, archive material, and run knowledge-base health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local note edits, archive moves, deletions, or index rewrites can damage or reorganize knowledge-base content unexpectedly. <br>
Mitigation: Review diffs before bulk edits and confirm archive, delete, and index rewrite actions before applying them. <br>
Risk: Sensitive credentials, customer data, or private business information could be added to notes. <br>
Mitigation: Keep secrets and private data out of the knowledge base and use placeholders for sensitive values. <br>
Risk: The configured wiki health check runs a local wiki-lint.js script in the user's environment. <br>
Mitigation: Inspect the local script before running it and set the intended scan directory explicitly when needed. <br>
Risk: Git commits or pushes could publish unintended knowledge-base changes. <br>
Mitigation: Check exactly what is staged and approve commits or pushes only after reviewing the change set. <br>


## Reference(s): <br>
- [HanSphere knowledge-base reference](references/hansphere.md) <br>
- [ClawHub skill page](https://clawhub.ai/otweihan/md-knowledge-base) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance, note content, file edits, relative links, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local knowledge-base reference configuration and should preserve Markdown front matter, dates, links, and naming conventions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
