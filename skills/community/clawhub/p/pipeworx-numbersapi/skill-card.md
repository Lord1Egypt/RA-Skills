## Description: <br>
NumbersAPI MCP connector that wraps numbersapi.com without requiring authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can add a remote MCP connector for number, date, math, and random trivia facts from NumbersAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and lookup queries are sent through a third-party remote MCP gateway. <br>
Mitigation: Use the skill only for data suitable for third-party network services, and avoid sending sensitive prompts or private information. <br>
Risk: The documented setup uses mcp-remote@latest, which can change over time. <br>
Mitigation: Pin the npm package version in local configuration when reproducibility or controlled change management matters. <br>


## Reference(s): <br>
- [Pipeworx NumbersAPI pack](https://pipeworx.io/packs/numbersapi) <br>
- [ClawHub release page](https://clawhub.ai/b-gutman/pipeworx-numbersapi) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a remote MCP gateway and mcp-remote bridge; no API key is documented.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
