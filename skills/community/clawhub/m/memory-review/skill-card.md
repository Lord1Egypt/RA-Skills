## Description: <br>
Memory Review scans recent diary entries, identifies durable knowledge, writes it to a memory knowledge base, and can generate and deliver a review report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AxelHu](https://clawhub.ai/user/AxelHu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to periodically review recent diary notes, extract reusable project knowledge, and maintain memory reports and knowledge files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated diary review and memory writes may persist incorrect, sensitive, or misleading knowledge. <br>
Mitigation: Use a dry-run or manual confirmation flow before enabling automation, and restrict writes to dedicated memory output paths. <br>
Risk: Automatic edits to agent-related files can alter future agent behavior. <br>
Mitigation: Avoid automatic TOOLS.md or AGENTS.md edits unless explicitly reviewed and approved. <br>
Risk: External report delivery can expose private report contents or send them to the wrong destination. <br>
Mitigation: Verify the Feishu destination and review report contents before sending. <br>


## Reference(s): <br>
- [Memory Review detailed specification](references/spec.md) <br>
- [Memory Review on ClawHub](https://clawhub.ai/AxelHu/memory-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, configuration, guidance] <br>
**Output Format:** [Markdown reports and knowledge files with execution-log state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes memory reports, knowledge entries, and execution logs; may read delivery configuration from AGENTS.md or MEMORY.md.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
