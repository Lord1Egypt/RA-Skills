## Description:

Screens Chinese-language health-product marketing copy for flagged therapeutic claims and missing medicine-substitution warnings, returning PASS or FAIL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and reviewers use this as a first-pass check of Chinese-language food and supplement copy for selected therapeutic phrases and missing warning language before publication; it is not legal or medical advice.

### Deployment Geography for Use:

Global (Chinese-language checks; assess local advertising requirements separately)

## Known Risks and Mitigations:

Risk: A limited Chinese-language phrase check can miss problematic claims or produce misleading compliance conclusions.

Mitigation: Treat results as preliminary screening and have qualified reviewers assess claims and required warnings before publication.

Risk: The documented --input command does not match the script's --text argument, and declared tool access exceeds the simple local checker’s needs.

Mitigation: Use the supported --text argument, limit allowed tools, and align declared permissions with actual runtime behavior.

## Reference(s):

- [Health Claim Guard release on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/health-claim-guard)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain-text PASS/FAIL assessment or JSON with pass, banned_hits and problems]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit code 0 for PASS, 1 for FAIL, and 2 for invalid arguments.]

## Skill Version(s):

1.0.4 (source: server release; bundled documentation says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
