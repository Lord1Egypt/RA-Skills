## Description:

Provides Wappalyzer search and read operations for requests involving Wappalyzer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to look up website technologies, discover subdomains, check email deliverability signals, and view the connected account's Wappalyzer credit balance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs unverified remote code and may change other agent skills.

Mitigation: Prefer a separately reviewed, pinned CLI installation and check which skills it installs or updates.

Risk: Requested domains and email addresses pass through OOMOL to Wappalyzer, and lookups may consume account credits.

Mitigation: Avoid submitting sensitive domains or email addresses, and check account credits before running large batches of lookups.

## Reference(s):

- [Wappalyzer](https://www.wappalyzer.com/)
- [Wappalyzer API documentation](https://www.wappalyzer.com/docs/api/v2/basics/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands]

**Output Format:** [Markdown guidance with inline shell commands and JSON response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific JSON inputs; lookup usage may consume account credits.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
