## Description: <br>
Wiza (wiza.co). Use this skill for Wiza requests, including reading, creating, and updating Wiza data through the OOMOL-connected `oo` CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Wiza through an OOMOL-connected account. It can inspect action schemas, check credits, retrieve reveal and list results, search prospects, and start individual contact enrichment after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a one-time CLI installer and OOMOL-brokered Wiza access. <br>
Mitigation: Review the `oo` CLI installation command before running it and install only when OOMOL should broker Wiza access. <br>
Risk: The `start_individual_reveal` action can change Wiza state or consume Wiza resources. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write actions. <br>
Risk: Using the wrong connected Wiza account or an expired connection can produce failed or unintended operations. <br>
Mitigation: Connect only the intended Wiza account and resolve connection, scope, or credential errors before retrying. <br>


## Reference(s): <br>
- [Wiza homepage](https://wiza.co) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-wiza) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the `oo` CLI to call Wiza connector actions; responses include connector data and an execution id.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
