## Description:

OSOP helps agents author, validate, risk-assess, execute, report on, and optimize Open Standard Operating Procedure workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archie0125](https://clawhub.ai/user/archie0125)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to define OSOP workflow YAML, review workflow risk, run or log workflow execution, generate HTML reports, and improve workflows from execution history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workflow and execution log files may contain secrets, internal paths, incident details, or infrastructure information.

Mitigation: Review .osop and .osoplog.yaml files before sharing, committing, or uploading them.

Risk: External visualization services may receive sensitive workflow or execution data.

Mitigation: Sanitize workflow and log files and obtain approval before uploading them to external viewers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/archie0125/skills/osop)
- [OSOP Website](https://osop.ai)
- [OSOP Spec](https://github.com/Archie0125/osop-spec)
- [OSOP Examples](https://github.com/Archie0125/osop-examples)
- [OSOP Visual Editor](https://osop-editor.vercel.app)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML, HTML report, Mermaid diagram, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce .osop workflow files and .osoplog.yaml execution logs; uses OSOP_MCP_URL and ~/.osop/config.yaml when configured.]

## Skill Version(s):

1.2.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
