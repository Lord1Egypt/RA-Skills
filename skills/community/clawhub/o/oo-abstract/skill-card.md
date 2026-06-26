## Description: <br>
Abstract lets an agent validate email addresses through an OOMOL-connected Abstract account using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to run Abstract email validation through an already connected OOMOL account. It guides the agent to inspect the live connector schema, submit a JSON payload, and return deliverability, quality, and risk check results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Abstract account and may rely on sensitive account credentials. <br>
Mitigation: Connect credentials only through the documented OOMOL/Abstract flow and avoid exposing raw tokens to the agent. <br>
Risk: Email validation queries are sent through OOMOL and Abstract services. <br>
Mitigation: Use the skill only for email data approved for processing by those services. <br>
Risk: First-time setup may require installing or authenticating an external CLI. <br>
Mitigation: Review the oo CLI install and authentication steps before running setup commands, and run setup only after a relevant command fails. <br>


## Reference(s): <br>
- [Abstract homepage](https://www.abstractapi.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The connector response is JSON containing data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
