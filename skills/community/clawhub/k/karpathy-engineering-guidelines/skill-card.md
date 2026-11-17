## Description:

Karpathy Guidelines provides engineering execution guardrails for coding, bug fixing, debugging, review, refactoring, planning, and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmvp3](https://clawhub.ai/user/gmvp3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to keep non-trivial software changes focused, evidence-driven, and verifiable while avoiding unnecessary abstractions and unrelated edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence how an agent approaches substantive coding tasks and may add process to larger tasks.

Mitigation: Apply it to non-trivial software engineering work and skip extra ceremony for trivial localized edits, as the skill directs.

Risk: Engineering guidance can still lead to incorrect changes if assumptions, skipped checks, or verification gaps are not made visible.

Mitigation: Require concrete local evidence before editing, keep changes scoped, and report verification results and remaining uncertainty.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with implementation plans, review notes, code snippets, shell commands, configuration suggestions, and verification steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code is included in the artifact; outputs are guidance for an agent's software engineering workflow.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
