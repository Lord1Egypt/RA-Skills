## Description: <br>
MinerU helps agents operate MinerU document extraction through OOMOL's oo CLI for reading, creating, and updating extraction tasks and batches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operations teams use this skill to create MinerU document extraction tasks or batches from document URLs and retrieve extraction status and result URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill submits document URLs and extraction requests through an OOMOL-connected MinerU account, so sensitive documents or extraction results may be exposed to that service. <br>
Mitigation: Confirm OOMOL and MinerU are trusted for the submitted documents and avoid sending confidential URLs unless the user has approved that handling. <br>
Risk: Task and batch creation actions can change MinerU state or consume credits. <br>
Mitigation: Inspect the live action schema, review the exact payload and effect with the user, and require confirmation before running write actions. <br>


## Reference(s): <br>
- [ClawHub MinerU Skill](https://clawhub.ai/oomol/oo-mineru) <br>
- [MinerU Homepage](https://mineru.net) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live MinerU action schemas before running connector commands; write actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
