## Description: <br>
Operates Jotform through an OOMOL-connected account using the oo CLI for reading account details, forms, questions, submissions, and creating submissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to operate Jotform data from an agent through the OOMOL connector. It supports reading account, form, question, and submission data, and creating submissions after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Jotform account and can read account, form, question, and submission data. <br>
Mitigation: Install it only for users or agents that should access that Jotform account, and keep the OOMOL connection scoped to the intended provider and account. <br>
Risk: The create_submission action changes Jotform state. <br>
Mitigation: Confirm the target form ID and exact submission payload with the user before running the write action. <br>
Risk: Server security evidence marks the bundle suspicious and recommends review before installation. <br>
Mitigation: Install only if the publisher is trusted and the Jotform workflow is needed; review the exact oo connector command and payload before allowing writes. <br>
Risk: The setup guidance includes remote CLI installation commands. <br>
Mitigation: Use an organization-approved installation path for the oo CLI and inspect remote install commands when policy requires it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-jotform) <br>
- [Jotform homepage](https://www.jotform.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL Jotform connection](https://console.oomol.com/app-connections?provider=jotform) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require an installed oo CLI, an authenticated OOMOL account, and a connected Jotform provider.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
