## Description:

Provides curated exploitation payloads for authorized security testing, including anti-virus test files, malicious files, and file name exploits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pandaai-1337](https://clawhub.ai/user/pandaai-1337)

### License/Terms of Use:

MIT-0

## Use Case:

Security testers, developers, and engineers use this skill to access curated payload examples for authorized anti-virus, file upload, path traversal, and security control validation tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dual-use payloads could be applied outside an authorized test scope.

Mitigation: Use only on systems where testing is permitted and align activity with the documented engagement scope.

Risk: The EICAR file is expected to trigger anti-virus and security monitoring alerts.

Mitigation: Coordinate with system owners before testing and isolate the payload in controlled test locations.

Risk: Null-byte and command-substitution filenames can cause unsafe behavior when copied into shell commands or upload tests.

Mitigation: Quote file paths, avoid evaluating filenames as commands, and run tests in disposable or controlled workspaces.

## Reference(s):

- [ClawHub Payloads skill page](https://clawhub.ai/pandaai-1337/skills/payloads)
- [Payloads README](references/Payloads/README.md)
- [File-Names README](references/Payloads/File-Names/README.md)
- [SecLists Payloads](https://github.com/danielmiessler/SecLists/tree/master/Payloads)
- [SecLists repository](https://github.com/danielmiessler/SecLists)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline file paths and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes static payload files and human-readable guidance for authorized security testing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
