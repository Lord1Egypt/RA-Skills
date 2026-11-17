## Description:

Marketing Site Dev guides agents through building a bilingual Astro, React, and Tailwind static company marketing site and deploying it to Volcengine TOS and CDN with HTTPS hardening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenshowinnovation](https://clawhub.ai/user/tenshowinnovation)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and implementation agents use this skill to scaffold a bilingual company or product marketing site and prepare a Volcengine-hosted static deployment for mainland-China audiences. It is best suited for teams with an ICP-filed domain and a need for TOS, CDN, DNS, certificate, and cache-invalidation guidance.

### Deployment Geography for Use:

China (mainland)

## Known Risks and Mitigations:

Risk: The skill requires cloud credentials for Volcengine deployment tasks.

Mitigation: Use dedicated least-privilege or temporary credentials scoped to the intended bucket, domain, DNS zone, CDN, and certificate operations.

Risk: Deployment scripts can remove storage objects that are not present in the local build output.

Mitigation: Use a dedicated bucket for this site, keep backups of existing content, and require a dry run or manual confirmation before upload and sync steps.

Risk: CDN and DNS setup can change domain records and production traffic routing.

Mitigation: Back up DNS records, review the generated domain and CNAME changes, and require explicit approval before CDN setup or DNS mutation.

## Reference(s):

- [Marketing Site Dev Skill Page](https://clawhub.ai/tenshowinnovation/skills/marketing-site-dev)
- [Landmines](references/landmines.md)
- [Phase 1 Static Site](references/phase-1-static-site.md)
- [Phase 2 Volcengine Deploy](references/phase-2-volcengine-deploy.md)
- [Verification Checklist](references/verification.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code, configuration, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May copy or adapt bundled static-site and Volcengine deployment templates into a user's project.]

## Skill Version(s):

0.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
