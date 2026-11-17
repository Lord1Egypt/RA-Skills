## Description:

Security Audit checks external resources such as GitHub repositories, downloaded skills, and files for malicious code, suspicious executables, and content mismatches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ithacajason](https://clawhub.ai/user/ithacajason)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to inspect cloned repositories, downloaded skills, and external files before running unfamiliar code. It provides static, heuristic findings that support manual security review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner may miss important malicious-file patterns while reporting that a project is safe.

Mitigation: Treat SAFE results as preliminary, run the tool only on the specific downloaded project or skill under review, and manually inspect findings before executing unfamiliar code.

Risk: Users may mistake the skill for a reliable security gate.

Mitigation: Present it as a lightweight static helper and require additional review for executables, obfuscated content, external scripts, and other high-risk inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ithacajason/skills/jason-security-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or terminal text with command examples and security findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are heuristic and require manual review before trusting or executing unfamiliar code.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
