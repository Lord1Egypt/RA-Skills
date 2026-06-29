## Description: <br>
Parseur (parseur.com). Use this skill for any Parseur request involving searching or reading mailbox and document data through the OOMOL oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to inspect Parseur mailboxes, mailbox schemas, and parsed document data through an OOMOL-connected Parseur account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Parseur account and may expose mailbox or document data through read actions. <br>
Mitigation: Install only when comfortable connecting Parseur through OOMOL, keep use to listed read actions, and review returned data handling before sharing outputs. <br>
Risk: Future write or destructive Parseur actions could change or remove data if added to the connector surface. <br>
Mitigation: Require separate review and explicit user approval before running any action tagged write or destructive. <br>
Risk: Remote CLI install commands are referenced for setup. <br>
Mitigation: Inspect remote install commands before running them and use setup steps only after a matching command failure. <br>


## Reference(s): <br>
- [Parseur homepage](https://parseur.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution and returns Parseur data through the oo CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
