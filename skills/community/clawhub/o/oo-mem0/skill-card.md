## Description: <br>
Mem0 connector skill for reading, creating, updating, and deleting Mem0 data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent operate an OOMOL-connected Mem0 account, including memory creation, retrieval, search, updates, deletion, history inspection, event listing, and user listing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an OOMOL-connected Mem0 account and can access account-backed memory, event, and user data. <br>
Mitigation: Install only for the intended Mem0 account and confirm the active OOMOL/Mem0 connection before use. <br>
Risk: Write and destructive actions can change or delete stored Mem0 memory data. <br>
Mitigation: Review exact action payloads before approving writes, and require explicit confirmation before running delete_memory. <br>


## Reference(s): <br>
- [Mem0 homepage](https://mem0.ai) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub Mem0 skill page](https://clawhub.ai/oomol/oo-mem0) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live oo connector schemas before action execution and returns JSON responses from the connector.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
