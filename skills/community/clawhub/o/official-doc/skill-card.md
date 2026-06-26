## Description: <br>
Official Doc helps users draft and review Chinese official documents, including notices, reports, requests, replies, format checks, tone checks, and templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users drafting Chinese administrative documents can use this skill to generate structured notices, reports, requests, and replies, then check format and formal tone against provided template guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An extra unrelated script can write a local command history and may retain sensitive names or arguments if run. <br>
Mitigation: Use the documented scripts/official.sh workflow; avoid running scripts/script.sh with secrets or sensitive internal names, and delete the local official-doc data directory if that history should not be retained. <br>


## Reference(s): <br>
- [Official Doc tips](tips.md) <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/official-doc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text document templates and review guidance, with Markdown documentation and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local CLI output; no external dependencies documented for the official document workflow.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
