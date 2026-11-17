## Description:

Checks loan disclosure text for an annualized-rate label and compares a supplied percentage rate with four times a supplied benchmark rate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Credit reviewers, compliance teams, and developers can screen Chinese-language loan marketing copy for an annualized-rate label and compare a supplied rate against a supplied benchmark. Results are a first-pass aid, not a lending or legal determination.

### Deployment Geography for Use:

Global (China-focused disclosure and benchmark assumptions)

## Known Risks and Mitigations:

Risk: Documentation overstates JSON/CSV input and automatic rate conversion.

Mitigation: Provide an already annualized rate through --rate and disclosure copy through --text; --json changes output format only.

Risk: The default benchmark may not reflect the current applicable rate.

Mitigation: Supply the current relevant benchmark explicitly with --base rather than relying on the default.

Risk: A screening result could be mistaken for a definitive legal or lending decision.

Mitigation: Keep a qualified legal or compliance reviewer in the loop for real lending decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhaoxinghua09-cell/skills/loan-rate-disclosure)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain text by default; JSON when --json is selected]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns checks and problems; exit code 0 for passing checks, 1 for failed checks, and 2 for invalid command-line input.]

## Skill Version(s):

1.0.4 (source: ClawHub release; bundled documentation says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
