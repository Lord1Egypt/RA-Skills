## Description:

Scans prompts and system prompts before sharing for secrets, internal paths, personal information, custom sensitive terms, and instructions that could expose a system prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other prompt publishers use this local scanner to check prompts for possible sensitive information or self-disclosure instructions before sharing them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented arguments differ from the current command-line interface.

Mitigation: Invoke the script directly with --text or --file and consult its --help output.

Risk: The skill manifest lists broader agent tools than the local scanner needs.

Mitigation: Avoid granting unnecessary WebFetch or Write access when scanning local prompts.

Risk: Medium-severity findings can still produce a zero exit code.

Mitigation: Review reported findings before sharing; do not treat exit code 0 alone as proof a prompt is safe.

## Reference(s):

- [Prompt Leak Scanner on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/prompt-leak-scanner)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Console text or JSON (--json)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit code 1 flags high-risk findings; exit code 0 can include medium-risk findings; exit code 2 indicates invalid input.]

## Skill Version(s):

1.0.4 (source: server-resolved ClawHub release; bundled skill frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
