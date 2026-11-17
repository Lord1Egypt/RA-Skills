## Description:

Automates NYC 311 service request filing with Playwright by scraping complaint categories, finding forms, filling them with user data, and optionally submitting reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pranjalminocha](https://clawhub.ai/user/pranjalminocha)

### License/Terms of Use:

MIT-0

## Use Case:

External users or agents assisting NYC residents use this skill to gather complaint details, browse the NYC 311 portal, and prepare or submit service requests through browser automation.

### Deployment Geography for Use:

New York City, United States

## Known Risks and Mitigations:

Risk: The skill handles personal contact and address data, and the artifact includes sample identity data in configuration and command examples.

Mitigation: Review and replace all sample identity data before use, and avoid storing real personal information in package-local configuration.

Risk: The browser automation can submit an official NYC 311 service request when run with the live submit option.

Mitigation: Run dry-run mode first, inspect the filled form and screenshots, and manually confirm the report before enabling live submission.

Risk: Screenshots saved under /tmp may contain complaint details or personal information.

Mitigation: Treat generated screenshots as sensitive and delete them after review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pranjalminocha/skills/nyc-311-reporter)
- [NYC 311 portal](https://portal.311.nyc.gov/)
- [NYC 311 report problems](https://portal.311.nyc.gov/report-problems/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with inline shell commands and JSON or text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save browser screenshots under /tmp for review.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
