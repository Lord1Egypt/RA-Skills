## Description:

Display the first lines of files. Use for quickly previewing file contents, checking headers, or sampling data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to preview the beginning of local text files, logs, CSVs, configuration files, or stdin before deciding whether to inspect more content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The implementation reads the full input before returning the requested first lines, which can cause unnecessary resource use on very large files or unbounded streams.

Mitigation: Use bounded files or streams for local previews until the implementation is changed to stop reading after the requested number of lines.

Risk: Some documented options are not implemented by the bundled script.

Mitigation: Verify actual command behavior before relying on byte-count mode, quiet mode, or multiple-file behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/head-tool)
- [Publisher profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text file previews with Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to the first 10 lines; the implementation supports a line-count option and single file or stdin input.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
