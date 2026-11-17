## Description:

Generate Prisma Access configurations for Strata Cloud Manager (SCM). Use when creating security policies, NAT rules, decryption policies, URL filtering profiles, GlobalProtect configs, or any SCM configuration objects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leesandao](https://clawhub.ai/user/leesandao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and network security engineers use this skill to draft SCM API-compatible JSON payloads for Prisma Access configuration objects, including policies, NAT, decryption, URL filtering, GlobalProtect, addresses, service connections, and related SCM objects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated security configurations may be incorrect, incomplete, or unsuitable for a production Prisma Access environment.

Mitigation: Review generated SCM API payloads carefully before applying them to production.

Risk: Prompts may include secrets or private authentication material while requesting configuration guidance.

Mitigation: Avoid putting secrets or private authentication material into prompts unless the environment is approved for that data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leesandao/skills/prisma-config)
- [Publisher Profile](https://clawhub.ai/user/leesandao)
- [Project Homepage](https://github.com/leesandao/prismaaccess-skill)
- [Strata Cloud Manager API Endpoint Pattern](https://api.sase.paloaltonetworks.com/sse/config/v1/{resource})

## Skill Output:

**Output Type(s):** [JSON, Configuration instructions, Guidance]

**Output Format:** [SCM API-compatible JSON payloads with endpoint paths, folder parameters, and query parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated configurations should be reviewed before production use.]

## Skill Version(s):

1.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
