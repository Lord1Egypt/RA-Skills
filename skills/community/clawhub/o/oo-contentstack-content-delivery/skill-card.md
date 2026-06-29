## Description: <br>
Contentstack Content Delivery lets agents search and read published Contentstack content through an OOMOL-connected account using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to let an agent inspect Contentstack content types, entries, and assets from an already connected OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may read more published Contentstack content than intended when a user request is broad or ambiguous. <br>
Mitigation: Confirm ambiguous requests before running connector actions and keep the OOMOL Contentstack connection limited to the intended account scope. <br>
Risk: Use depends on installing the oo CLI and connecting an OOMOL account before content can be accessed. <br>
Mitigation: Review the oo CLI installer and account connection flow before first use, then run setup only when an auth or connection command fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-contentstack-content-delivery) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Contentstack Content Delivery homepage](https://www.contentstack.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash snippets and JSON connector responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the oo CLI and an OOMOL account connection for Contentstack Content Delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
