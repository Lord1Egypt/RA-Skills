## Description:

Crawl a bounded same-origin site and report broken links, missing fragments, duplicate titles and image alt omissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT-0

## Use Case:

Site owners and developers can use the skill to run a bounded audit of an authorized website and review link, fragment, title, and image-alt issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional external checks contact linked sites, and redirects may leave the starting site.

Mitigation: Audit only sites you are authorized to assess; keep external checks disabled unless they are needed, and review the bounded request scope.

Risk: Allowing private-host access can direct requests to private or reserved network addresses.

Mitigation: Leave private-host access disabled unless it is necessary for the authorized audit.

## Reference(s):

- [Action contract](references/input.md)
- [MochiLab homepage](https://mochilab.bz)
- [ClawHub skill release](https://clawhub.ai/hznetnewpower/skills/mochi-link-audit)

## Skill Output:

**Output Type(s):** [Analysis, JSON, HTML report, CSV]

**Output Format:** [Structured audit results with local JSON, HTML, and CSV report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bounded to 1–60 same-origin pages; optional external-link checks are separately bounded.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
