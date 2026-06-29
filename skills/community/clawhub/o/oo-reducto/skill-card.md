## Description: <br>
Reducto helps agents parse documents, extract structured JSON, and split documents into named page sections through an OOMOL-connected Reducto account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route Reducto document-processing requests through an OOMOL-connected account for parsing, schema-based extraction, and document sectioning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document-processing requests are routed through an OOMOL-connected Reducto account, which may be inappropriate for sensitive documents unless the user's policies allow that processing. <br>
Mitigation: Use the skill only with documents approved for Reducto and OOMOL processing under the user's account, data-handling, and compliance policies. <br>
Risk: First-time setup may require installing the OOMOL oo CLI from a remote installer. <br>
Mitigation: Review the remote installer and install the oo CLI only from trusted OOMOL sources before using the skill. <br>


## Reference(s): <br>
- [ClawHub Reducto Skill](https://clawhub.ai/oomol/skills/oo-reducto) <br>
- [Reducto](https://reducto.ai) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, JSON, Text] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before execution so action payloads match Reducto's current contract.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
