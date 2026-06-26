## Description: <br>
Prerender (prerender.io) manages reading, creating, updating, and deleting Prerender data through OOMOL instead of direct API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Prerender account actions through OOMOL, including sitemap submission, cache clearing, cache status checks, and URL recaching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit sitemaps, clear cache entries, and recache URLs in a connected Prerender account. <br>
Mitigation: Confirm the exact payload, target URLs, wildcard patterns, and expected effect with the user before running write or destructive actions. <br>
Risk: The skill depends on the local oo CLI and OOMOL-managed credentials. <br>
Mitigation: Install or update the oo CLI only from the trusted OOMOL source and run first-time authentication or connection steps only after a command fails for that specific reason. <br>


## Reference(s): <br>
- [ClawHub Prerender Skill](https://clawhub.ai/oomol/oo-prerender) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Prerender Homepage](https://prerender.io) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce oo CLI connector commands and JSON payload guidance for Prerender actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
