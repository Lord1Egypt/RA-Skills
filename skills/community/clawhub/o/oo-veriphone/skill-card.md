## Description:

Veriphone. Use this skill for ANY Veriphone request — searching and reading data. Whenever a task involves Veriphone, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill through their OOMOL-connected account to check phone-number validity and retrieve carrier and region details, or to view account verification credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified downloaded code and make broader, persistent changes to agent skills.

Mitigation: Review and install a verified CLI release separately; set OO_SKILLS_SYNC_DISABLED=1 when only Veriphone access is needed.

Risk: Phone numbers are sent to OOMOL and Veriphone for verification.

Mitigation: Submit only phone numbers you are authorized to share with OOMOL and Veriphone.

## Reference(s):

- [Veriphone API documentation](https://veriphone.io/docs)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON connector responses with concise natural-language summaries; shell commands for action invocation and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Phone verification results may include validity, carrier, and region data; credit queries return an account credit summary.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
