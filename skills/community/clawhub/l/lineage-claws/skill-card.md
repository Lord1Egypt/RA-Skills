## Description: <br>
The trust gate for MO§ES governance, providing origin verification so audit chains can be checked against a filing anchor before they are trusted. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SunrisesIllNeverSee](https://clawhub.ai/user/SunrisesIllNeverSee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, auditors, and agent operators use this skill to initialize and verify MO§ES audit-chain lineage, emit human-readable custody status, and produce machine-readable pass/fail checks for integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat local hash-chain checks as signed attestation, legal custody proof, or independently verified provenance. <br>
Mitigation: Use the skill output as local integrity metadata only, and separately validate provenance, signatures, legal custody, and CI trust-gate requirements before relying on it for security or governance decisions. <br>
Risk: Initialization and archival commands create or read local state under ~/.openclaw, which can affect subsequent verification results on the same machine. <br>
Mitigation: Run the commands in a controlled workspace or review the ~/.openclaw governance and audit files before using the results as evidence. <br>


## Reference(s): <br>
- [Lineage Custody Clause](references/LineageCustodyClause.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/SunrisesIllNeverSee/lineage-claws) <br>
- [Publisher Profile](https://clawhub.ai/user/SunrisesIllNeverSee) <br>
- [Zenodo Record](https://zenodo.org/records/18792459) <br>
- [MO§ES Site](https://mos2es.io) <br>
- [GitHub Project Link](https://github.com/SunrisesIllNeverSee/moses-claw-gov) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration, Text, JSON] <br>
**Output Format:** [Markdown guidance with bash command snippets; bundled scripts emit terminal text, JSON attestation data, and process exit codes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local governance and audit state under ~/.openclaw when initialization or archival commands are run.] <br>

## Skill Version(s): <br>
0.4.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
