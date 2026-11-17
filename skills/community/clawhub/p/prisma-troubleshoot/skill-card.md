## Description:

Troubleshoot Prisma Access issues including GlobalProtect connectivity, policy matching, tunnel status, SCM API errors, and configuration push failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leesandao](https://clawhub.ai/user/leesandao)

### License/Terms of Use:

MIT-0

## Use Case:

Network security operators and engineers use this skill to diagnose Prisma Access connectivity, policy matching, tunnel, SCM API, performance, and configuration push issues. It helps structure troubleshooting, identify likely causes, and propose verification steps or relevant SCM API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a candidate configuration push API call as part of troubleshooting, and the security evidence warns that this can affect live Prisma Access configuration.

Mitigation: Require explicit change approval before any candidate push, and treat push commands as proposed remediation steps rather than routine status checks.

Risk: The skill depends on SCM credentials for Prisma Access troubleshooting.

Mitigation: Use least-privilege SCM credentials and avoid granting push permissions for read-only troubleshooting workflows.

## Reference(s):

- [Prisma Access Skill Homepage](https://github.com/leesandao/prismaaccess-skill)
- [ClawHub Skill Page](https://clawhub.ai/leesandao/skills/prisma-troubleshoot)
- [ClawHub Publisher Profile](https://clawhub.ai/user/leesandao)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with diagnostic steps and inline SCM API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference SCM credentials and live configuration workflows that require operator approval.]

## Skill Version(s):

1.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
