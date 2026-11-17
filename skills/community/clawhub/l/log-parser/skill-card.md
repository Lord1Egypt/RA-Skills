## Description:

Parse and analyze various log formats (nginx, apache, syslog, application logs). Extract key information and generate reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freeter226](https://clawhub.ai/user/freeter226)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, and security analysts use this skill to parse local nginx, Apache, syslog, and JSON application logs, then produce structured summaries, filters, error extracts, and top-value reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parsed logs and JSON outputs may contain secrets, personal data, internal hostnames, or session identifiers.

Mitigation: Review and redact parser output before sharing it outside the intended analysis context.

Risk: Very large log files may cause slow execution or excessive memory use because the parser reads the file into memory.

Mitigation: Run the parser on bounded log samples or rotated files when analyzing large production logs.

Risk: The skill reads local log files supplied by path.

Mitigation: Provide only log paths that the agent is authorized to inspect.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freeter226/skills/log-parser)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON from the bundled parser, with Markdown guidance and shell command examples for agent-facing use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3. Reads only log files explicitly provided to the parser command.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
