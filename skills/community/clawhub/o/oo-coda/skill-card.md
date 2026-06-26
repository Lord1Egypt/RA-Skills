## Description: <br>
Coda lets agents read, create, and update Coda data through an OOMOL-connected account instead of calling the Coda API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect live Coda connector schemas, read Coda docs, pages, tables, columns, and rows, and perform confirmed write actions such as creating pages or upserting rows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup guidance includes running a remote installer directly in a shell. <br>
Mitigation: Review and verify the official oo CLI installation path before installation, inspect installer contents where possible, and do not let an agent run the pipe-to-shell setup automatically. <br>
Risk: The skill can perform write actions that change Coda state. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running actions tagged as write or destructive. <br>
Risk: The connector requires authenticated access to a Coda account. <br>
Mitigation: Use the OOMOL-connected account flow and avoid exposing raw Coda API tokens to the agent. <br>


## Reference(s): <br>
- [ClawHub Coda Skill](https://clawhub.ai/oomol/oo-coda) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>
- [Coda Homepage](https://coda.io) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are expected as JSON when commands are run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
