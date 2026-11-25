## Description:

Audit user-provided HTTP response headers for common security-header and cookie-flag issues without fetching URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nenadzivotic](https://clawhub.ai/user/nenadzivotic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site owners can review response headers they provide from DevTools or saved output to spot common missing hardening headers and cookie flags, then use concise suggestions to improve them. The checks reflect common conventions rather than a compliance standard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented curl example makes a live request despite the offline-only description; scan coverage was incomplete and does not establish fetching behavior inside the script or malicious intent.

Mitigation: If an offline audit is intended, provide saved or pasted headers directly and omit the curl request. Review the conflicting example and the incomplete scan guidance before installing or using the skill.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/nenadzivotic/skills/http-header-audit-lite)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON audit report with concise Markdown findings and suggested fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts header text from a file or standard input. Checks common hardening conventions; it is not a compliance assessment.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
