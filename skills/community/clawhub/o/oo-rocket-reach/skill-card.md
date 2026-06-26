## Description: <br>
RocketReach helps agents search and read RocketReach account, person, and company data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to inspect RocketReach action schemas and run account-connected people, company, and account lookups through the oo CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RocketReach queries can expose person, company, and account-profile data available to the connected OOMOL account. <br>
Mitigation: Review the live action schema and payload before sending lookup or search data, and only query data the user is authorized to access. <br>
Risk: Setup and login steps connect a RocketReach account and may use sensitive credentials managed through OOMOL. <br>
Mitigation: Run setup or login only when the user intends to connect RocketReach or when an action fails with an authentication or connection error. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-rocket-reach) <br>
- [RocketReach Homepage](https://rocketreach.co) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
