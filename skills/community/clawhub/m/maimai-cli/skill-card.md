## Description: <br>
maimai-cli guides agents in using the local Maimai CLI to manage login state, read feeds and hot lists, search content, inspect details and comments, download images, and troubleshoot CLI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariotong](https://clawhub.ai/user/mariotong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route Maimai-related requests to the correct `maimai` CLI commands while preserving login and short-index handling rules. It supports authenticated reading, search, detail inspection, comments, image downloads, and troubleshooting through concise command guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Maimai cookies or session values could be exposed if users paste credentials into chat or if raw command output is repeated unnecessarily. <br>
Mitigation: Have users import cookies in their own terminal, avoid echoing stored credentials, and recommend logout or re-login if a complete cookie is exposed. <br>
Risk: The skill can guide authenticated CLI actions that read feeds, comments, profiles, and images or write downloaded files locally. <br>
Mitigation: Review commands before execution, start with small result limits, and use raw output or downloads only when the user explicitly needs them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mariotong/maimai-cli) <br>
- [Project homepage](https://github.com/mariotong/maimai-cli) <br>
- [Authentication and security](references/auth.md) <br>
- [Feed and list reading](references/feeds.md) <br>
- [Search and discovery](references/search.md) <br>
- [Details, comments, images, and profiles](references/detail.md) <br>
- [Troubleshooting and workflows](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend JSON, YAML, or raw CLI output only when the user requests scriptable or diagnostic output.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
