## Description: <br>
OKSign connector support for reading OKSign account, user, document, and signed-document metadata through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect OKSign account credits, users, active documents, linked document IDs, and signed-document metadata through OOMOL's OKSign connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected OKSign account, and the agent can read account, user, and document metadata visible to that account. <br>
Mitigation: Install only when the publisher is trusted, connect the minimum appropriate OKSign account, and review requested actions before allowing access to sensitive document metadata. <br>
Risk: Authentication, connection, or billing recovery flows can redirect the user into account setup or recharge steps. <br>
Mitigation: Run setup or recovery commands only after an oo CLI command fails with the matching authentication, connection, scope, credential, app, or billing error. <br>
Risk: Future connector actions or schemas may include write or destructive operations even though the listed actions are read-only. <br>
Mitigation: Fetch the live action schema before building a payload and require explicit user confirmation for any action tagged write or destructive. <br>


## Reference(s): <br>
- [ClawHub OKSign skill page](https://clawhub.ai/oomol/oo-oksign) <br>
- [OKSign homepage](https://www.oksign.be/en/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector actions return JSON data with a meta.executionId when executed through the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
