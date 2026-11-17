## Description:

AI-orchestrated usability testing using Amazon Nova Act that generates personas, collects browser-test data, interprets goal achievement, and produces HTML usability reports for real user workflows with safety guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zouchaoqun](https://clawhub.ai/user/zouchaoqun)

### License/Terms of Use:

MIT

## Use Case:

Developers, QA teams, and UX reviewers use this skill to run persona-based browser usability tests against authorized websites, inspect raw Nova Act responses, and generate HTML reports with findings and trace links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate actions on live websites, including commerce, account, posting, and form workflows.

Mitigation: Use only websites you are authorized to test, preferably staging or sandbox environments, and stop before actions with monetary, legal, reputational, or account impact.

Risk: Nova Act traces and generated reports may contain screenshots, page content, and other sensitive data from tested sites.

Mitigation: Treat traces and reports as sensitive files, avoid pages containing PII or confidential data, and review or delete generated artifacts after testing.

Risk: Security evidence recommends review before installation because the skill has incomplete scoping around external data sharing, generated reports, dependencies, and runner reliability.

Mitigation: Review the skill and dependencies before deployment, pin dependency versions where appropriate, and validate the test runner in a disposable environment before relying on results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zouchaoqun/skills/nova-act-usability)
- [Nova Act Cookbook](references/nova-act-cookbook.md)
- [Persona Examples](references/persona-examples.md)
- [AWS Console](https://console.aws.amazon.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, shell commands, JSON test results, HTML usability reports, and Nova Act trace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Nova Act API key and Python/Playwright dependencies; writes reports and traces into the working directory.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
