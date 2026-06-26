## Description: <br>
Linear (linear.app) lets agents read, create, update, and delete Linear data through the OOMOL Linear connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and project teams use this skill to read, create, update, and delete Linear workspace data through a schema-first CLI workflow. It supports common Linear issue, comment, attachment, label, project, milestone, cycle, team, user, and workflow-state operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Linear workspace access can change business data beyond the curated action list, including through direct GraphQL mutation access. <br>
Mitigation: Install only if broad Linear access through the OOMOL connection is acceptable; prefer curated actions, review any run_mutation payload carefully, and require explicit approval before writes or deletions. <br>
Risk: Write and destructive actions can create, update, remove, or overwrite Linear records. <br>
Mitigation: Confirm the exact target, payload, and expected effect with the user before running write or destructive actions. <br>


## Reference(s): <br>
- [ClawHub Linear skill page](https://clawhub.ai/oomol/oo-linear) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Linear homepage](https://linear.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before execution; command responses are returned as JSON by the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
