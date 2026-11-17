## Description:

Automatically solve Moltbook verification challenges (math problems) when posting by parsing obfuscated number text and calculating answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pickmemory](https://clawhub.ai/user/pickmemory)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agents use this skill to solve Moltbook posting verification challenges that encode math problems in obfuscated text. It can return a calculated answer locally and, when explicitly configured with a verification code and API key, submit the answer to Moltbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional submission path sends a user-provided API key and verification answer to Moltbook.

Mitigation: Use submission only with an API key intended for Moltbook verification, and prefer local answer calculation when submission is not needed.

Risk: Automated verification attempts may conflict with Moltbook rate limits, posting rules, or terms of service.

Mitigation: Review Moltbook's rules before use, add delays between attempts, and stop automation when rate limited.

Risk: Moltbook challenge wording or obfuscation patterns may change, causing incorrect answers.

Mitigation: Manually review failed or unusual challenges and update the solver test corpus before relying on new patterns.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pickmemory/skills/moltbook-verification-solver)
- [Moltbook API endpoint](https://www.moltbook.com/api/v1)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance, API calls]

**Output Format:** [Plain text CLI output, Python integration snippets, and JSON API response objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit a verification answer to Moltbook only when the caller provides a verification code, API key, and submit flag.]

## Skill Version(s):

1.0.3 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
