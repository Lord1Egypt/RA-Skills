## Description: <br>
Operates Tomba through an OOMOL-connected account for domain email discovery, email verification, enrichment, company search, LinkedIn contact lookup, and technology detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run Tomba searches, verification, enrichment, account lookup, company search, and technology detection through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Tomba account and sensitive credentials managed through OOMOL. <br>
Mitigation: Use a scoped OOMOL/Tomba connection and follow the setup guidance so raw tokens are not handled directly. <br>
Risk: Tomba lookups can return personal or company contact data. <br>
Mitigation: Run only the requested lookup actions and review results for privacy, policy, and contractual handling requirements before sharing. <br>


## Reference(s): <br>
- [ClawHub Tomba skill page](https://clawhub.ai/oomol/oo-tomba) <br>
- [Tomba homepage](https://tomba.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can execute Tomba connector actions through the oo CLI and return JSON responses when requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
