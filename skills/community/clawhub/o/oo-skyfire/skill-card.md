## Description: <br>
Skyfire lets an agent operate Skyfire through an OOMOL-connected account for marketplace reads and buyer token creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to inspect Skyfire marketplace services and create buyer tokens through the OOMOL Skyfire connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create Skyfire buyer tokens that may involve funds or identity attributes. <br>
Mitigation: Confirm the exact write payload and expected effect with the user before running token creation. <br>
Risk: Connector requests may fail or behave unexpectedly if the live Skyfire action schema changes. <br>
Mitigation: Inspect the live connector schema before building each action payload. <br>
Risk: The skill requires an authenticated OOMOL-connected Skyfire account. <br>
Mitigation: Use first-time setup or connection recovery only after an action fails with an authentication or connection error. <br>


## Reference(s): <br>
- [Skyfire Skill Page](https://clawhub.ai/oomol/oo-skyfire) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [Skyfire Homepage](https://skyfire.xyz) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce connector command payloads for marketplace reads or buyer token creation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
