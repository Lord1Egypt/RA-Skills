## Description: <br>
Operate Neon projects, branches, databases, operations, and current-user reads through the OOMOL-connected oo CLI Neon connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and manage Neon resources from an agent session through an OOMOL-connected account. It supports routine reads as well as schema-checked create, update, and delete actions for Neon projects, branches, and databases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, and delete Neon projects, branches, and databases. <br>
Mitigation: Review the live action schema, exact target, and payload before approving write actions; require explicit approval for destructive delete actions. <br>
Risk: The skill depends on an OOMOL account connection and the locally installed oo CLI to access Neon resources. <br>
Mitigation: Install only when OOMOL-managed Neon access is intended, and trust the OOMOL account connection and oo CLI installation source before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-neon) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Neon homepage](https://neon.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads; command responses are JSON when run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
