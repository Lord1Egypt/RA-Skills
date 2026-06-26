## Description: <br>
Controls a local Chrome or Edge browser through the page-agent CLI over CDP, with installation currently documented from GitHub release .tgz artifacts rather than the public npm registry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdyuyouth](https://clawhub.ai/user/sdyuyouth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to inspect browser tabs, index interactive page elements, perform CDP-backed browser actions, and capture reusable site experience notes for repeat workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install and use an external global CLI release. <br>
Mitigation: Install only from a trusted, independently verified page-agent CLI release source before enabling the skill. <br>
Risk: Browser automation can operate against a normal logged-in browser profile through a remote debugging port. <br>
Mitigation: Prefer a separate browser profile without sensitive logins and enable remote debugging only while the workflow is active. <br>
Risk: The browser workflow can reach high-impact actions such as posting, buying, deleting, uploading, or submitting data. <br>
Mitigation: Require explicit human confirmation before any high-impact action is executed. <br>
Risk: Optional LLM run mode may expose page content to configured model services. <br>
Mitigation: Avoid LLM run mode unless the operator understands what page data may be sent to the configured endpoint. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdyuyouth/page-agent-browser) <br>
- [Publisher Profile](https://clawhub.ai/user/sdyuyouth) <br>
- [page-agent CLI Releases](https://github.com/sdyuyouth/page-agent-cli/releases) <br>
- [CLI Reference](artifact/CLI_REFERENCE.md) <br>
- [Architecture](artifact/ARCHITECTURE.md) <br>
- [Critical Actions](artifact/CRITICAL_ACTIONS.md) <br>
- [Experience Schema](artifact/EXPERIENCE_SCHEMA.md) <br>
- [Exploration Protocol](artifact/EXPLORATION_PROTOCOL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON workflow notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide browser actions through an externally installed page-agent CLI; teach workflows can produce JSON lesson output after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
