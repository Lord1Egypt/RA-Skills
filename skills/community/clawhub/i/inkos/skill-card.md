## Description: <br>
InkOS helps agents create and manage long-form and short-form story projects through Studio Chat, CLI, and TUI workflows, including writing, research, covers, interactive play, auditing, and project analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[narcooo](https://clawhub.ai/user/narcooo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, authors, and agent operators use InkOS to orchestrate story-writing projects, persistent canon/state, research reports, cover generation, interactive fiction sessions, and exportable creative deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: InkOS can access and modify a user's local writing project and generated files. <br>
Mitigation: Install only when comfortable granting that access, keep generated project files under review, and review delete, rewrite, update, or daemon actions before they run. <br>
Risk: Configured AI, search, image, or custom provider endpoints may receive project content or API keys. <br>
Mitigation: Keep API keys in environment variables or service settings, use only trusted custom base URLs, and keep secret files out of commits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/narcooo/skills/inkos) <br>
- [Publisher profile](https://clawhub.ai/user/narcooo) <br>
- [Project homepage](https://github.com/Narcooo/inkos) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and text with inline shell commands, JSON-style tool results, and project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local story project files and may call user-configured AI, search, or image providers.] <br>

## Skill Version(s): <br>
2.5.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
