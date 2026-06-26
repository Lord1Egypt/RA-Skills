## Description: <br>
Generates Markdown drafts of GPU compute leasing or sales contracts from parameters such as client name, GPU model, quantity, price, and duration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashiming](https://clawhub.ai/user/dashiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to draft Chinese-language GPU or AI compute lease agreements for review before business and legal approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated contract language may be incomplete, inaccurate, or unsuitable for a specific transaction or jurisdiction. <br>
Mitigation: Treat each draft as a starting template and have qualified legal counsel review it before use. <br>
Risk: The command can write the generated contract to a user-provided output path. <br>
Mitigation: Choose the output path deliberately and review the generated Markdown file before sharing or relying on it. <br>


## Reference(s): <br>
- [Pans Contract Generator on ClawHub](https://clawhub.ai/dashiming/pans-contract-generator) <br>
- [Standard GPU Lease Template](references/templates/standard_gpu_lease.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown contract draft, printed to stdout or written to a user-selected file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally and uses required CLI parameters for client, GPU model, quantity, price, and duration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
