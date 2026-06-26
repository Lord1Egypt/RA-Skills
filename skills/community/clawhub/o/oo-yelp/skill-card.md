## Description: <br>
Yelp (yelp.com) support for searching and reading Yelp business data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Yelp businesses, retrieve business details, and look up businesses by phone through an OOMOL-connected Yelp account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Yelp account and server-side credential injection. <br>
Mitigation: Install and use it only when OOMOL is an acceptable intermediary for Yelp access, and confirm the OOMOL account connection before use. <br>
Risk: First-time setup commands install or authenticate the oo CLI and may affect the user's local environment. <br>
Mitigation: Run setup, authentication, connection, or billing commands only after the matching connector error occurs. <br>
Risk: Connector input schemas can change over time. <br>
Mitigation: Inspect the live action schema with oo connector schema before constructing each JSON payload. <br>


## Reference(s): <br>
- [ClawHub Yelp skill page](https://clawhub.ai/oomol/oo-yelp) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Yelp homepage](https://www.yelp.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses include data and a meta.executionId value.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
