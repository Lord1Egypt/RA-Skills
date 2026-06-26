## Description: <br>
Patents MCP wraps the PatentsView API for patent and inventor lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search patents, retrieve patent details, and search inventors through the Pipeworx Patents MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent searches route through Pipeworx's remote MCP gateway. <br>
Mitigation: Avoid sending confidential invention details unless the user trusts the Pipeworx service and its handling of search data. <br>
Risk: The setup command uses an unpinned npm bridge through npx. <br>
Mitigation: Review and pin the bridge package version in managed environments before installation. <br>


## Reference(s): <br>
- [Pipeworx Patents](https://pipeworx.io/packs/patents) <br>
- [PatentsView API](https://api.patentsview.org/) <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-patents) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a remote Pipeworx MCP gateway and does not require an API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
