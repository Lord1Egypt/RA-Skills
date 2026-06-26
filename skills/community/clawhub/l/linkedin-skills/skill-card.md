## Description: <br>
LinkedIn automation skill collection for authentication, content publishing, feed browsing, search and discovery, social interactions, and compound operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ceoqveda](https://clawhub.ai/user/ceoqveda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate LinkedIn through a local browser extension and Python CLI, including login checks, feed and profile exploration, publishing, engagement, lead generation, and multi-step content workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Python bridge and Chrome extension can control a real logged-in LinkedIn session. <br>
Mitigation: Use a dedicated Chrome profile, keep the bridge disabled when not in use, and install only when this level of local account access is acceptable. <br>
Risk: Posts, comments, messages, and connection requests may affect the user's public LinkedIn account. <br>
Mitigation: Personally confirm every publish, comment, message, connection, or other account-changing action before execution. <br>
Risk: Untrusted local software could attempt to interact with localhost services used by the bridge. <br>
Mitigation: Avoid running the skill on machines where untrusted local processes may connect to local services. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ceoqveda/linkedin-skills) <br>
- [Publisher Profile](https://clawhub.ai/user/ceoqveda) <br>
- [uv Documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI output summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, Google Chrome, a locally installed Chrome extension, and user confirmation for publishing or social actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata; pyproject.toml reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
