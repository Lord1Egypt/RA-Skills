## Description: <br>
BidSketch uses the OOMOL connector to let agents search, read, and retrieve BidSketch client or proposal data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to inspect BidSketch clients and proposals from an OOMOL-connected account, including proposal content and client-specific proposal lists. It is intended for read-oriented BidSketch workflows where the agent should fetch the live action schema before running connector commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a visible CLI installer command that can modify the user's shell or CLI environment. <br>
Mitigation: Review the OOMOL CLI installer source or use the official install guide or package manager before running installation commands. <br>
Risk: The skill requires a connected BidSketch account and sensitive credentials managed through OOMOL. <br>
Mitigation: Run connector actions only in an environment where the user has intentionally connected BidSketch, and do not request or handle raw BidSketch tokens. <br>


## Reference(s): <br>
- [BidSketch homepage](https://www.bidsketch.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses include BidSketch data and an execution ID when actions run successfully.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
