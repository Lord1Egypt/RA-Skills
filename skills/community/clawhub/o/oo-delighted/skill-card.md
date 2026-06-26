## Description: <br>
Operate Delighted through an OOMOL-connected account to read, create, update, delete, and unsubscribe Delighted people and retrieve metrics and survey data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to manage Delighted account data through the OOMOL oo CLI, including metrics, people, bounced or unsubscribed lists, survey responses, and guarded write or destructive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a connected Delighted account through the OOMOL oo CLI. <br>
Mitigation: Install and use it only when OOMOL CLI access to the Delighted account is intended. <br>
Risk: Create or update actions can change Delighted account data. <br>
Mitigation: Review the exact JSON payload and expected effect before approving write actions. <br>
Risk: Delete and unsubscribe actions can remove survey history or suppress future contact. <br>
Mitigation: Confirm the target person and get explicit approval before running destructive actions. <br>


## Reference(s): <br>
- [ClawHub Delighted skill page](https://clawhub.ai/oomol/oo-delighted) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Delighted homepage](https://delighted.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
