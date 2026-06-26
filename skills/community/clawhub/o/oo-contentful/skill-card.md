## Description: <br>
Contentful helps agents read, create, and update Contentful CMS data through the OOMOL oo CLI connector instead of direct API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and agent users use this skill to inspect Contentful users, spaces, environments, content types, and entries, and to create or update entries after reviewing the live connector schema and confirming write payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and update Contentful entries, which may change CMS content. <br>
Mitigation: Confirm the exact write payload and expected effect with the user before running create_entry or update_entry. <br>
Risk: The optional first-time setup path includes a pipe-to-shell CLI installer. <br>
Mitigation: Verify the oo CLI installer source before running the install command, or use the documented install guide. <br>
Risk: The skill requires an OOMOL-connected Contentful account and sensitive credentials managed by the service. <br>
Mitigation: Install only when the publisher is trusted and the user is comfortable connecting their Contentful account through OOMOL. <br>


## Reference(s): <br>
- [ClawHub Contentful Skill](https://clawhub.ai/oomol/oo-contentful) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>
- [Contentful](https://www.contentful.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON payload or response handling.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands call oo connector actions and may return JSON data from Contentful.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
