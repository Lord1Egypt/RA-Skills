## Description:

Use when working with .phiproto files, PhiProto messages, or converting between .phiproto and CSV with the bundled phicli binary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengongpp](https://clawhub.ai/user/chengongpp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect, decode, encode, validate, explain, and convert PhiProto message files between .phiproto and CSV formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and executes an unverified phicli binary into $HOME/.local/bin.

Mitigation: Install only after reviewing and trusting the upstream release; prefer a reviewed, pinned, checksum- or signature-verified binary before use.

Risk: The install script can replace an existing phicli command in $HOME/.local/bin without prompting.

Mitigation: Check for an existing phicli binary before running the script and require explicit approval before replacing it.

Risk: The documented runtime is limited to Linux x86_64.

Mitigation: Use the skill only on Linux x86_64 systems or provide a reviewed platform-specific binary for other environments.

## Reference(s):

- [PhiProto CLI ClawHub release](https://clawhub.ai/chengongpp/skills/phiproto)
- [phicli release binary](https://github.com/chengongpp/phiproto/releases/download/0.0.2/phicli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and generated .csv or .phiproto files when conversion is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Linux x86_64 phicli execution; decoded output may be written to stdout or to an explicit output file.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
