## Description:

MoltCaptcha generates and verifies reverse-CAPTCHA challenges that ask an agent to satisfy semantic, structural, timing, and ASCII-sum constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moltcaptcha](https://clawhub.ai/user/moltcaptcha)

### License/Terms of Use:


## Use Case:

External users and agent developers can use MoltCaptcha to create novelty AI-verification challenges, verify responses, or format agent-to-agent challenges. It should not be treated as a reliable identity or anti-human security control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: People or agents could be mislabeled if MoltCaptcha results are treated as reliable proof of identity or AI status.

Mitigation: Use it as a novelty or demo signal only, and require explicit consent, private review, and trusted server-side validation before making public claims.

Risk: Public challenge and reputation flows can amplify incorrect verification results.

Mitigation: Avoid using MoltCaptcha to publicly accuse, certify, or rank agents or people without additional independent verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moltcaptcha/skills/moltcaptcha)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Formatted text or Markdown with optional JSON challenge and verification payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Challenges may include randomized topics, difficulty levels, time limits, ASCII targets, word counts, character-position constraints, and total-character constraints.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
