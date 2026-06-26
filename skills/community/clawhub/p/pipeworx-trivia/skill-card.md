## Description: <br>
Trivia questions from the Open Trivia Database - 4,000+ questions across 24 categories with difficulty levels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch public trivia questions, categories, and category statistics for quiz games, educational apps, team activities, and interactive question prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends public trivia requests to the Pipeworx gateway. <br>
Mitigation: Use it only where that external endpoint is trusted and allowed by network policy. <br>
Risk: The example MCP configuration installs mcp-remote with an @latest version selector. <br>
Mitigation: Pin mcp-remote to a reviewed version before enabling the MCP configuration in managed environments. <br>


## Reference(s): <br>
- [Pipeworx Trivia Homepage](https://pipeworx.io/packs/trivia) <br>
- [Pipeworx Trivia MCP Endpoint](https://gateway.pipeworx.io/trivia/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with JSON and bash snippets; MCP tool responses return trivia question data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports optional category, difficulty, question type, and amount filters; no credential environment variables are declared.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
