## Description: <br>
DocuSeal helps agents read document templates and create DocuSeal signature submissions through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect DocuSeal action schemas, list or retrieve templates, and create signature submissions after confirming write payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials through the connected DocuSeal account. <br>
Mitigation: Use the existing OOMOL credential flow and avoid exposing raw tokens in prompts, command output, or files. <br>
Risk: The create_submission action changes DocuSeal state and may send signature requests. <br>
Mitigation: Inspect the live action schema and confirm the exact payload, recipients, and intended effect with the user before running write actions. <br>


## Reference(s): <br>
- [DocuSeal homepage](https://www.docuseal.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-docuseal) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash, PowerShell, and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector action responses are JSON objects with data and meta.executionId when commands run.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
