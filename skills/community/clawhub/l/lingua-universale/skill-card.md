## Description: <br>
Verify agent-to-agent communication against session type protocols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rafapra3008](https://clawhub.ai/user/rafapra3008) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and agent builders use this skill to parse Lingua Universale protocol definitions, verify whether agent messages follow session-type protocols, check declared safety properties, and browse protocol templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Python MCP package installation may introduce supply-chain risk through package sources or dependencies. <br>
Mitigation: Install from a trusted package source and pin or review dependencies when strict supply-chain control is required. <br>
Risk: Protocol checks can confirm conformance to a supplied protocol, but they do not prove the protocol itself is appropriate for every business workflow. <br>
Mitigation: Review protocol definitions and declared properties before using verification results to gate agent communication. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rafapra3008/lingua-universale) <br>
- [Lingua Universale project homepage](https://github.com/rafapra3008/cervellaswarm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON strings from MCP tools, plus Markdown documentation with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API keys are required; verification runs locally through an MCP server.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter, pyproject.toml, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
