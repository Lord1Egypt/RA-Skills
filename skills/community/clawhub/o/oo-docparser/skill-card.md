## Description: <br>
Operates Docparser through an OOMOL-connected account for reading, creating, and updating Docparser data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to work with Docparser through the OOMOL connector, including importing documents, retrieving parser data and parsed results, checking document status, and scheduling reprocessing or integration queue work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some Docparser import, reparse, reintegrate, or enqueue actions can change remote service state. <br>
Mitigation: Before executing those actions, show the exact action name and payload and get user confirmation. <br>
Risk: The skill requires a connected Docparser account and sensitive credentials handled by the OOMOL connector. <br>
Mitigation: Use the connector-authenticated account only for intended Docparser tasks and follow the setup flow only after an authentication or connection failure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-docparser) <br>
- [Docparser homepage](https://docparser.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live connector schema before action execution and returns connector responses as JSON when commands are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
