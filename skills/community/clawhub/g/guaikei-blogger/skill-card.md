## Description:

guaikei-blogger helps an agent query public Xiaohongshu data, including keyword search, note details and comments, and blogger post lists, then return structured JSON for content and market analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, marketers, content operators, and data analysts use this skill to retrieve public Xiaohongshu search results, note/comment details, and blogger post lists for topic research, competitor monitoring, KOL screening, and report preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu URLs, search terms, returned public content, and the GUAIKEI_API_TOKEN to the Guaikei service.

Mitigation: Use only when data sharing with Guaikei is acceptable, keep the token in environment variables, and rotate the token if it is exposed.

Risk: Saved logs may contain full links, access parameters, comments, and profile or post data.

Mitigation: Treat logs as sensitive, run the skill in a private workspace, avoid committing logs, and delete or secure saved outputs after use.

Risk: Untrusted URLs can expose unexpected access parameters or unsupported targets before URL validation is reviewed.

Mitigation: Prefer known Xiaohongshu or xhslink URLs and manually check hostnames before running commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-blogger)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with bash command examples and structured JSON results from the Node.js scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; script results may be saved under logs/ with links, request parameters, comments, and profile or post data.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
