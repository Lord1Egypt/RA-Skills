## Description: <br>
Keygen (keygen.sh). Use this skill for ANY Keygen request: reading, creating, updating, and deleting data through the OOMOL connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Keygen products, policies, licenses, users, groups, entitlements, machines, components, and processes from an agent. It supports read operations as well as state-changing account workflows when the user has connected Keygen through OOMOL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route broad read, write, and destructive actions into a connected Keygen account. <br>
Mitigation: Require clear user intent before account-impacting actions and explicit confirmation for actions tagged write or destructive. <br>
Risk: The skill requires sensitive account credentials through the connector. <br>
Mitigation: Install only when the user intends to let the agent access Keygen through OOMOL, and rely on the connector's server-side credential handling rather than exposing raw API tokens. <br>


## Reference(s): <br>
- [ClawHub Keygen skill listing](https://clawhub.ai/oomol/oo-keygen) <br>
- [Keygen homepage](https://keygen.sh) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The agent should inspect the live connector schema before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
