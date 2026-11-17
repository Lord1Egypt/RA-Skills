## Description:

CUFinder (cufinder.io). Use this skill for ANY CUFinder request — searching and reading data. Whenever a task involves CUFinder, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use CUFinder to look up company and professional information, including company and person enrichment and company name or domain searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required oo CLI can silently install additional agent skills during startup.

Mitigation: Review the CLI's installation effects; if only CUFinder access is needed, set OO_SKILLS_SYNC_DISABLED=1 before invoking oo and independently review the installer and installed version.

Risk: Lookup data is shared with OOMOL and CUFinder and may be subject to usage charges.

Mitigation: Submit only data authorized for sharing with both services and check applicable usage charges.

## Reference(s):

- [CUFinder](https://cufinder.io)
- [CUFinder API documentation](https://apidoc.cufinder.io/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [CUFinder on ClawHub](https://clawhub.ai/oomol/skills/oo-cufinder)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON results with concise text guidance; shell commands invoke CUFinder actions through oo.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the oo CLI, an authenticated OOMOL account, and a connected CUFinder account; inspect each action schema before sending a request.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
