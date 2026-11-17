## Description:

Jsonpretty formats, validates, queries, flattens, and analyzes JSON data from files or stdin using a zero-dependency Python utility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogue-agent1](https://clawhub.ai/user/rogue-agent1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Jsonpretty to inspect JSON files or piped JSON, including pretty-printing, validation, dot-notation queries, flattening, structure statistics, compact output, and sorted keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Formatting, flattening, querying, or statistics output can expose sensitive values when the input JSON contains secrets.

Mitigation: Review JSON inputs before running the utility and avoid printing secret-bearing data to shared terminals, logs, or transcripts.

## Reference(s):

- [ClawHub Jsonpretty skill page](https://clawhub.ai/rogue-agent1/skills/jsonpretty)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Markdown with shell command examples and JSON or plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read JSON from files or stdin; command output can include values from the source JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
