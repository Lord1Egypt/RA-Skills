## Description:

Searches LinkedIn for candidates matching user-defined role, location, and criteria, classifies hard and soft requirements, and saves profile summaries to avoid duplicate scans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qianjunye](https://clawhub.ai/user/qianjunye)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, sourcers, and hiring teams use this skill to clarify candidate requirements, search LinkedIn profiles, evaluate role and location fit, and save candidate records for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup can expose sensitive Chrome profile data if normal browser Cookies or Login Data are copied into the debug profile.

Mitigation: Use a fresh dedicated Chrome profile for LinkedIn and log in manually instead of copying normal Chrome profile data.

Risk: A Chrome remote debugging session can expose browser access if it is reachable beyond the local machine.

Mitigation: Bind debugging to localhost and close the debug browser session when the search is complete.

Risk: LinkedIn profile data is saved locally under ./linkedin-save/.

Mitigation: Review, protect, and delete saved profile files according to the organization's candidate-data handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qianjunye/skills/linkedin-search)
- [Publisher profile](https://clawhub.ai/user/qianjunye)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with tables, inline shell commands, browser-check instructions, and saved profile files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves LinkedIn profile summaries under ./linkedin-save/ and reports candidate match levels.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
