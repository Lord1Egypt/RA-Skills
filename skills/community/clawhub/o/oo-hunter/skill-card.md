## Description: <br>
Hunter enables agents to read, create, update, and delete Hunter data through an OOMOL-connected account instead of calling the Hunter API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to work with Hunter account data from an agent, including domain search, email finding and verification, enrichment, and lead/list management. It supports both read workflows and confirmed state-changing lead operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run Hunter write and destructive actions that create, update, upsert, or delete lead records. <br>
Mitigation: Confirm the exact payload, target, and effect with the user before write actions, and require explicit approval before destructive actions. <br>
Risk: The skill depends on sensitive account credentials and a connected Hunter provider account. <br>
Mitigation: Install and use it only for authorized accounts, rely on the connected-account flow, and avoid exposing raw credentials in prompts or command payloads. <br>
Risk: Connector action schemas may change over time. <br>
Mitigation: Inspect the live action schema before constructing each payload so commands match the authoritative input and output contract. <br>


## Reference(s): <br>
- [ClawHub Hunter Skill](https://clawhub.ai/oomol/oo-hunter) <br>
- [Hunter Homepage](https://hunter.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed oo CLI, an authenticated OOMOL account, and a connected Hunter provider account.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
