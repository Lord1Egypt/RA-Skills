## Description: <br>
Benzinga helps agents search and read Benzinga market data through OOMOL's oo CLI connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to query Benzinga market data, analyst ratings, earnings events, news channels, and related read-only data through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Benzinga account or API key through OOMOL. <br>
Mitigation: Install and use it only when the user is comfortable with OOMOL's oo CLI and OOMOL-managed Benzinga credentials. <br>
Risk: First-time setup commands install or authenticate the oo CLI. <br>
Mitigation: Review the oo CLI installer before running setup, and run authentication or connection steps only after an auth or connection failure. <br>
Risk: Future connector versions could add write or destructive actions. <br>
Mitigation: Keep using the skill for the listed read-only Benzinga actions unless a future version clearly adds write actions and the user confirms the exact payload and effect. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-benzinga) <br>
- [Benzinga homepage](https://www.benzinga.com/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON objects that include data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
