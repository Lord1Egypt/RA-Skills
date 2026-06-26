## Description: <br>
Analyzes a codebase to generate project-specific context files for Claude, OpenClaw/Codex, Cursor, Windsurf, and GitHub Copilot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect a repository and generate context files that help AI coding assistants follow the project's stack, structure, conventions, and test workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects repository files and may surface sensitive project details in generated assistant context files. <br>
Mitigation: Install it only in repositories the user is comfortable having an assistant inspect, and review generated files before approving writes. <br>
Risk: Generated instructions could embed real secrets or grant future agents overly broad permissions. <br>
Mitigation: Review CLAUDE.md, AGENTS.md, .cursorrules, .windsurfrules, and Copilot instructions before use, with particular attention to secrets and allowed operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-ai-context-gen) <br>
- [Canlah AI](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files and concise implementation guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates CLAUDE.md, AGENTS.md, .cursorrules, .windsurfrules, and .github/copilot-instructions.md after inspecting repository evidence.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
