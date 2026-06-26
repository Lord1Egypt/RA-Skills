## Description: <br>
Semantic Scholar helps agents search, retrieve, and recommend research papers, authors, citations, references, and snippets through the OOMOL Semantic Scholar connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and research assistants use this skill to query Semantic Scholar from an agent workflow, including paper search, author lookup, citation and reference retrieval, title matching, snippets, and paper recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connecting Semantic Scholar credentials through OOMOL and uses OOMOL as an intermediary for requests. <br>
Mitigation: Install and use it only when that intermediary model is acceptable, and connect credentials only through the documented OOMOL setup path when needed. <br>
Risk: First-time setup may require installing the oo CLI before connector actions can run. <br>
Mitigation: Review the oo CLI installation step before running it, and perform login or connection setup only after an authentication or connection failure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-semantic-scholar) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>
- [Semantic Scholar homepage](https://www.semanticscholar.org/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses include a data payload and execution metadata when actions are run with JSON output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
