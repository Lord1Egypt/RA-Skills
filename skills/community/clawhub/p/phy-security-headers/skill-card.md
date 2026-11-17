## Description:

HTTP security header auditor that fetches response headers from a URL, grades common browser security headers, and suggests nginx, Apache, Next.js, or Cloudflare Workers fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and DevOps teams use this skill to audit HTTP response security headers on live URLs or local services and receive prioritized configuration fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unrestricted URL fetching can cause the agent to probe local or private network services.

Mitigation: Run audits only against domains or local services you control, and add URL allowlisting plus private-network protections before broad use.

Risk: Outbound curl requests run from the user's machine or agent runtime.

Mitigation: Use this skill only in environments where outbound network requests to the target URL are acceptable and monitored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-security-headers)
- [Canlah AI homepage](https://canlah.ai)
- [HSTS preload list](https://hstspreload.org)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with tables and inline bash, nginx, Apache, JavaScript, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include security grades, prioritized findings, and generated configuration snippets.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
