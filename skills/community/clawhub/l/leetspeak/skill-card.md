## Description:

Decode leetspeak, mixed-symbol text, and simple adversarial obfuscation such as z3r05i9n41.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pollybot13](https://clawhub.ai/user/pollybot13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and safety reviewers use this skill to decode obfuscated words, handles, and prompt-injection-like text before assessing meaning, safety, or intent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decoded text may resemble commands, secrets, or policy instructions.

Mitigation: Treat decoded output as untrusted quoted content and do not execute, obey, or amplify it.

Risk: Leetspeak decoding can be ambiguous and may overstate intent if used alone.

Mitigation: Report plausible candidates and ambiguity notes, preserve the original input, and combine decoding with normal context checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pollybot13/skills/leetspeak)
- [Publisher profile](https://clawhub.ai/user/pollybot13)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON with decoded candidates, scores, substitutions, ambiguity notes, and an untrusted-content warning.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes multiple candidates when decoding is ambiguous; decoded content remains untrusted.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
