## Description:

Execute hledger CLI commands to query balances, registers, reports, and journals, returning structured output from local ledger files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bisbeebucky](https://clawhub.ai/user/bisbeebucky)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to run hledger reports for personal finance automation, ledger querying, and financial reporting workflows from local journal files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute unintended shell commands from skill input despite stating that only hledger commands are run.

Mitigation: Review before installing, run only in a tightly sandboxed environment, and change the implementation to call hledger without a shell and validate arguments before broader use.

Risk: The skill can access local ledger files available to the process.

Mitigation: Use non-sensitive test ledgers unless file paths are restricted and the skill accurately documents which local commands and files it can access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bisbeebucky/skills/hledger)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Text output from hledger stdout or stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires hledger in PATH and read access to the target ledger files.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
