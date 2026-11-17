## Description:

GitGuard helps agents audit local Git repositories for exposed secrets, repo health, commit quality, stale branches, dependency freshness, and GitHub PR or issue backlog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[welove111](https://clawhub.ai/user/welove111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit repositories they own or are authorized to assess, prioritize cleanup work, and triage repository maintenance signals across one or more projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can follow symlinks and may inspect readable files outside the selected repository, which could expose private file snippets in results.

Mitigation: Run it only on repositories you control and trust, avoid symlinks in untrusted repositories, or execute it in a sandbox limited to the target repository.

Risk: Dependency checks, GitHub triage, and optional token use involve network-enabled reads and may touch private repository metadata when configured that way.

Mitigation: Verify the remote MCP endpoint before use, scope any GitHub token narrowly, and avoid sending private repository data to endpoints you have not reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/welove111/skills/gitguard)
- [Project homepage](https://btc-vision.org)
- [Project repository](https://github.com/welove111/gitguard-skill)
- [MCP endpoint](https://github.com/welove111/gitguard-skill/.netlify/functions/mcp)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON-compatible dictionaries with human-readable summaries, scores, findings, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Secret findings are returned with redacted previews; dependency freshness and GitHub triage may use network reads.]

## Skill Version(s):

1.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
