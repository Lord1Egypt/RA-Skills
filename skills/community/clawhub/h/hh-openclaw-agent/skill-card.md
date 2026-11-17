## Description:

HH OpenClaw Agent helps prepare a reviewed hh.ru application packet, execute the logged-in browser flow through OpenClaw, and capture an auditable submission bundle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to prepare vacancy-specific hh.ru application packets, record approved browser execution steps, validate the bundle, and render a shareable submission report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can assist a logged-in hh.ru application flow, so an unreviewed packet could result in unintended live submission.

Mitigation: Review and approve the application packet before any submit action; the bundle checker flags submitted steps unless review status is approved.

Risk: Authentication challenges such as login, CAPTCHA, passkey, or 2FA may appear during browser execution.

Mitigation: Stop automation for authentication challenges and have the operator complete them in the logged-in browser profile.

Risk: Submission reports may expose cover letters, private paths, or non-public URLs if sensitive export is requested.

Mitigation: Use the default report mode for sharing; it redacts cover letters, private paths, and non-hh.ru URLs unless sensitive output is intentionally enabled.

Risk: Reports generated from untrusted or externally edited manifests can be misleading.

Mitigation: Run the bundle checker and review validation findings before relying on or sharing a generated report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/skills/hh-openclaw-agent)
- [Project homepage](https://github.com/zack-dev-cm/hh-openclaw-agent)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown]

**Output Format:** [Markdown guidance with shell commands, JSON packet and validation files, and a Markdown submission report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 or python; reports redact cover letters, private paths, and non-hh.ru URLs by default.]

## Skill Version(s):

1.0.7 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
