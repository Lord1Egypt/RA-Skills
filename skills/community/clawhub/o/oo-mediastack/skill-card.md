## Description: <br>
Mediastack lets agents search live news and news sources through an OOMOL-connected account using the oo CLI instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search live Mediastack news articles and news sources through an OOMOL-connected Mediastack account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the OOMOL CLI and an OOMOL-connected Mediastack account. <br>
Mitigation: Install and authenticate the OOMOL CLI only when needed, and use it for Mediastack news-reading workflows with a trusted OOMOL account. <br>
Risk: Credential or billing errors can prevent connector actions from running. <br>
Mitigation: Follow the documented setup, connection, and billing recovery steps only after an action fails with the matching error. <br>


## Reference(s): <br>
- [ClawHub Mediastack skill page](https://clawhub.ai/oomol/oo-mediastack) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Mediastack homepage](https://mediastack.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live connector schema before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
