## Description:

Lint AI prompts for clarity, safety, injection risks, and template validity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, prompt engineers, agent builders, and AI product teams use this skill to check prompt files for missing role, goal, output-format cues, vague wording, jailbreak phrases, and template-quality issues before use in workflows or CI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install documentation fetches executable code from a mutable GitHub URL.

Mitigation: Use the bundled prompt_lint.py file, or download only from a pinned commit and verify the file hash before execution.

Risk: The bundled verifier can execute Python files from submissions under review.

Mitigation: Run ci/verify_product.py only in an isolated environment without secrets, network access, or writable sensitive files.

Risk: The current CLI behavior may not be suitable as a CI-blocking safety gate.

Mitigation: Use the lint output as advisory review input unless exit-code behavior is fixed and validated for the intended CI policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itspremkumar/skills/prompt-lint)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-capable CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stdlib Python CLI that can return a prompt quality score and issue list; no external service is required.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
