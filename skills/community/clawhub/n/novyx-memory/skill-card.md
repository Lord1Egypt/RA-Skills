## Description: <br>
Enterprise-grade persistent memory for AI agents with rollback, audit trails, knowledge graph, governed actions, time-travel debugging, and 60+ Novyx Core commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[novyxlabs](https://clawhub.ai/user/novyxlabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use Novyx Memory to give agents persistent conversation memory, semantic recall, rollback, audit history, knowledge graph features, shared context spaces, and policy-controlled memory operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation content and assistant responses may be sent to Novyx for persistent storage and future recall. <br>
Mitigation: Avoid secrets, regulated data, customer records, and sensitive internal material unless Novyx retention, deletion, sharing, and access controls meet your requirements. <br>
Risk: Automatic save and recall can persist or reuse context without an explicit command. <br>
Mitigation: Review the deployment configuration and disable autoSave or autoRecall where persistent storage or context injection is not appropriate. <br>
Risk: Rollback, delete, and share commands can alter or expose stored memory state. <br>
Mitigation: Limit use of memory-changing and sharing commands to trusted operators and review their effects before using them in sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/novyxlabs/novyx-memory) <br>
- [Novyx Labs](https://novyxlabs.com) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown command responses, recalled memory context, JavaScript integration code, shell commands, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NOVYX_API_KEY; autoSave and autoRecall are enabled by default unless configured otherwise.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
