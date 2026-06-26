## Description: <br>
Plisio (plisio.net) enables an agent to operate Plisio through OOMOL, including creating hosted invoices, checking balances, and retrieving or listing operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage Plisio merchant workflows from an agent, including hosted invoice creation and read access to balances, operations, and invoices. Write actions should be reviewed with the user before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create hosted Plisio invoices, which changes merchant workflow state. <br>
Mitigation: Confirm the exact invoice payload and intended effect with the user before running the write action. <br>
Risk: The skill depends on an authenticated OOMOL connection to Plisio and may require sensitive account credentials managed outside the skill. <br>
Mitigation: Use server-side credential injection through OOMOL and avoid handling raw Plisio API tokens directly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-plisio) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Plisio homepage](https://plisio.net) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses oo CLI connector calls and returns connector JSON responses when actions are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
