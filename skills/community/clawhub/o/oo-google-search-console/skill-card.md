## Description: <br>
Google Search Console connector skill for reading, creating, updating, and deleting Google Search Console data through the OOMOL oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and SEO operators use this skill to manage Search Console properties and sitemaps, inspect URL indexing status, and query search analytics through an OOMOL-connected Google account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write and destructive actions can change or remove Google Search Console properties or submitted sitemaps. <br>
Mitigation: Confirm the exact action, target property or sitemap, payload, and expected effect with the user before running tagged write or destructive commands. <br>
Risk: The skill depends on an OOMOL account, the oo CLI, and a connected Google Search Console credential. <br>
Mitigation: Use first-time setup only after an authentication or connection failure, and do not ask the user to provide raw Google tokens. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-google-search-console) <br>
- [Google Search Console](https://search.google.com/search-console) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL Google Search Console connection](https://console.oomol.com/app-connections?provider=google_search_console) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches the live connector schema before building payloads; write and destructive actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata, SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
