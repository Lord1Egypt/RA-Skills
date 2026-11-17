## Description:

Smart auto-reply for GitHub Issues with professional customer service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sendwealth](https://clawhub.ai/user/sendwealth)

### License/Terms of Use:


## Use Case:

Developers and repository maintainers use this skill to configure GitHub issue auto-replies that acknowledge new issues, choose response templates by issue type, and communicate response expectations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated replies may post public comments with incorrect, premature, or unintended customer-facing text.

Mitigation: Review and customize the reply templates before installation, especially contact details, response-time commitments, and issue-type language.

Risk: The workflow can run in repositories where automated public issue comments are not intended.

Mitigation: Restrict the GitHub Actions workflow to the intended repositories and issue events before enabling it.

Risk: Broad GitHub Actions settings or unreviewed action versions can increase workflow supply-chain and permission risk.

Mitigation: Use explicit minimal workflow permissions and pin the GitHub Action to a reviewed commit or approved version policy.

## Reference(s):

- [GitHub Auto Reply ClawHub Skill Page](https://clawhub.ai/sendwealth/skills/github-auto-reply)
- [Claw Intelligence Publisher Site](https://sendwealth.github.io/claw-intelligence/)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with GitHub Actions YAML and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes configurable reply templates, label-based template selection examples, multilingual response examples, and work-hour response behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
