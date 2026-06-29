## Description: <br>
Operate Google Routes through an OOMOL-connected account to compute routes and route matrices using the oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect Google Routes connector schemas and run route or route-matrix calculations through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route locations and related request data are sent through OOMOL's connector to Google Routes. <br>
Mitigation: Confirm trust in OOMOL and review live schemas and payloads before sending route data. <br>
Risk: Setup, login, or connection commands can change the user's local environment or account connection state. <br>
Mitigation: Run oo CLI install, login, or connection steps only after a matching command failure indicates they are needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/skills/oo-google-routes) <br>
- [Google Routes Documentation](https://developers.google.com/maps/documentation/routes) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector action responses are JSON objects containing data and meta.executionId when commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
