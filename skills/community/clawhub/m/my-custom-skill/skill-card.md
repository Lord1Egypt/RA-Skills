## Description: <br>
Infinite organized memory that complements an agent's built-in memory with unlimited categorized storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardyjcool](https://clawhub.ai/user/edwardyjcool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create and maintain a local long-term memory system for projects, contacts, decisions, domain knowledge, collections, and other structured notes that grow over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-lived local notes may accumulate sensitive personal, financial, health, account, or project information. <br>
Mitigation: Review what is saved, avoid storing secrets unless explicitly intentional, and periodically delete or prune old memory files. <br>
Risk: Copied built-in memory can duplicate or preserve information longer than intended. <br>
Mitigation: Use the optional sync deliberately, copy only information that benefits from long-term organization, and keep built-in memory as the source for short summaries. <br>
Risk: Large or stale memory indexes can make retrieval slower or misleading. <br>
Mitigation: Maintain category indexes, split large categories, archive inactive entries, and remove outdated content during regular reviews. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/edwardyjcool/my-custom-skill) <br>
- [Skill homepage](https://clawic.com/skills/memory) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Setup guide](artifact/setup.md) <br>
- [Memory templates](artifact/memory-template.md) <br>
- [Organization patterns](artifact/patterns.md) <br>
- [Troubleshooting](artifact/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated local markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates user-controlled markdown notes under ~/memory when the user chooses to use the memory system.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
