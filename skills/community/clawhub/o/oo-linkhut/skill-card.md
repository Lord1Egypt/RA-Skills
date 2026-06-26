## Description: <br>
Linkhut (ln.ht) helps an agent read, create, update, and delete Linkhut bookmarks through the OOMOL oo CLI instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage Linkhut bookmarks through an OOMOL-connected account. It supports reading bookmarks and tags, plus confirmed create, update, and delete actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, or delete Linkhut bookmarks through the connected OOMOL account. <br>
Mitigation: Require explicit user approval for write and destructive actions, including the exact payload and target bookmark. <br>
Risk: First-time setup may require installing and authenticating the OOMOL oo CLI before the connector can access Linkhut. <br>
Mitigation: Review the oo CLI installer before setup and connect only the intended Linkhut account. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-linkhut) <br>
- [Linkhut Homepage](https://ln.ht) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live connector schema before each action and requires explicit confirmation for write or destructive bookmark changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
