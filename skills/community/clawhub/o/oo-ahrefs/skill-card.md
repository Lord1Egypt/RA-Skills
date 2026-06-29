## Description: <br>
Ahrefs (ahrefs.com). Use this skill for ANY Ahrefs request - searching and reading data. Whenever a task involves Ahrefs, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve Ahrefs keyword, usage, and site metrics through an OOMOL-connected account without handling raw credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may act on the wrong Ahrefs target or request shape if it skips schema inspection. <br>
Mitigation: Inspect the connector action schema before constructing payloads and confirm ambiguous domains, URLs, keywords, or countries with the user. <br>
Risk: The skill depends on an authenticated OOMOL-connected Ahrefs account and may fail when credentials, scopes, or billing are unavailable. <br>
Mitigation: Use the documented first-time setup and connection recovery steps only after an auth, scope, credential, app, or billing error occurs. <br>
Risk: Security evidence advises installing this package only in an intended operational environment. <br>
Mitigation: Deploy it only where the agent is expected to use connected operational services, and review targets before any sensitive or administrative action. <br>


## Reference(s): <br>
- [Ahrefs homepage](https://ahrefs.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-ahrefs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to inspect live connector schemas before running read-only Ahrefs actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
