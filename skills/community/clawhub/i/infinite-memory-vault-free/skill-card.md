## Description: <br>
与Agent内置记忆并行的无限组织化记忆免费版：自定义分类、索引导航、即写即存。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create and maintain an organized local memory vault in ~/memory/ for projects, contacts, decisions, knowledge notes, and other long-running context that may outgrow built-in agent memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause an agent to store personal, customer, credential-adjacent, or confidential business information in a durable local memory vault without clear consent boundaries. <br>
Mitigation: Require explicit confirmation before saving sensitive information, keep the vault scoped to intended content, and review or delete stored memory regularly. <br>
Risk: Long-lived local memory can become stale, duplicated, or misleading if indexes are not maintained. <br>
Mitigation: Review INDEX.md files and archived entries on a regular schedule before relying on stored context for decisions. <br>


## Reference(s): <br>
- [Detailed examples](references/detail.md) <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/infinite-memory-vault-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and filesystem paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory organization instructions and examples; does not require API keys or network access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
