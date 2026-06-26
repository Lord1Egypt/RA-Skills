## Description: <br>
Mao Colleague helps agents analyze questions, recommend Mao Zedong-inspired methods, guide progressive learning paths, and query a concept knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[friendfish](https://clawhub.ai/user/friendfish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to apply Mao Zedong methodology to analysis, learning, concept lookup, method comparison, and style-aware guidance through agent commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad local file and shell permissions. <br>
Mitigation: Install it only in a project-scoped or sandboxed environment and review requested file or shell actions before allowing execution. <br>
Risk: Bundled maintenance scripts can modify or delete files. <br>
Mitigation: Do not run internal maintenance scripts unless their target paths and effects have been reviewed. <br>
Risk: Dependency installation may introduce additional supply-chain exposure. <br>
Mitigation: Pin, review, or sandbox Python dependencies before running pip install. <br>
Risk: Mao-framed analysis and unclear logging or progress tracking may be inappropriate for sensitive content. <br>
Mitigation: Avoid entering sensitive personal, political, legal, or private business information unless that framing and local state behavior are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/friendfish/mao-colleague) <br>
- [README.en.md](README.en.md) <br>
- [Detailed Guide](docs/user/detailed_guide.md) <br>
- [Command Cheat Sheet](docs/user/cheat_sheet.md) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with command examples, structured analysis, learning guidance, and concept explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Mao-framed analysis, learning-path recommendations, concept lookup results, command suggestions, and settings guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
