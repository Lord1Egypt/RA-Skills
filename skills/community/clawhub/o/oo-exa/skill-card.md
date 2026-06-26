## Description: <br>
Exa helps agents search the web, generate citation-backed answers, find similar pages, and retrieve page contents through OOMOL-connected Exa actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to perform Exa web search, citation-backed answering, similar-page discovery, and content retrieval without handling raw Exa API tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive service credentials through an OOMOL-connected Exa account. <br>
Mitigation: Use the managed OOMOL connection flow, avoid exposing raw API tokens, and reconnect only when an authentication or connection error requires it. <br>
Risk: The skill runs shell commands that access external Exa and OOMOL services. <br>
Mitigation: Inspect the live connector schema and payload before execution, and review the skill files before use when high assurance is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-exa) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Exa homepage](https://exa.ai) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON when commands are run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
