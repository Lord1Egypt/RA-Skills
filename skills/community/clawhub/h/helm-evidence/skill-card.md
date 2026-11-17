## Description:

Check and verify AI-number figures from extracted reviewer files with Helm, offline via helmd. Never paste raw extract numbers; quote exit codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[collectrix](https://clawhub.ai/user/collectrix)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, reviewers, and audit teams use this skill to run local helmd checks against reviewer extract files, verify signed bundles with public keys, and report file references with command exit codes rather than raw extracted numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An untrusted helmd binary or unintended reviewer extract file could produce misleading verification results.

Mitigation: Install helmd from a trusted source and point it only at the local reviewer extract files intended for the check.

Risk: Raw extracted numbers may expose review details or make results harder to audit if pasted into chat.

Mitigation: Report the input file reference and helmd exit code instead of copying raw extract numbers.

Risk: A bundle could be described as valid without signature verification.

Mitigation: Run helmd verify with the intended public keys and cite exit code 0 before making a VALID claim.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/collectrix/skills/helm-evidence)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports local file references and helmd exit codes; avoids pasting raw extract numbers.]

## Skill Version(s):

2026.8.18 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
