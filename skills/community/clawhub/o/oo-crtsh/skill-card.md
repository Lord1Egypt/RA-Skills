## Description:

crt.sh (crt.sh). Use this skill for ANY crt.sh request — searching and reading data. Whenever a task involves crt.sh, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security practitioners use the skill to search crt.sh certificate transparency records for certificates matching a domain, including wildcard subdomain searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup runs a remote installer, and CLI startup may synchronize other agent skills.

Mitigation: Review and pin the CLI before installing it; use the documented startup-sync control and inspect changes to other skills.

Risk: Certificate queries pass through OOMOL and may incur charges.

Mitigation: Check applicable OOMOL charges before querying.

## Reference(s):

- [crt.sh](https://crt.sh)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-crtsh)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [JSON certificate search results with shell command instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are capped by the requested limit.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
