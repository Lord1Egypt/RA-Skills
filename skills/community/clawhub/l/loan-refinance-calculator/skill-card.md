## Description:

Calculates loan refinance scenarios through a paid remote API, estimating interest savings, monthly payment changes, payback period, and recommended refinance options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g620710](https://clawhub.ai/user/g620710)

### License/Terms of Use:

MIT

## Use Case:

External loan advisors and financial service teams use this skill to produce refinance comparisons for customers, including estimated savings, monthly payment changes, payback period, product suggestions, and operational notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends sensitive loan and account data to a remote paid SaaS endpoint, and the default endpoint uses HTTP.

Mitigation: Use only a verified HTTPS endpoint with clear privacy, retention, and billing terms; avoid submitting real customer loan details through the default endpoint.

Risk: The skill requires a user key and consumes paid credits for calculations.

Mitigation: Use a dedicated key, restrict access to the environment variable, and monitor credit usage before production workflows.

Risk: Security evidence reports that the shipped script appears syntactically broken.

Mitigation: Fix the script and repeat security and functionality review before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/g620710/skills/loan-refinance-calculator)
- [Default backend API endpoint](http://47.109.39.255:8765/api/v4)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote paid API client; calculations require REFINANCE_USER_KEY and consume account credits.]

## Skill Version(s):

1.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
