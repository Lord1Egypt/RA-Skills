## Description: <br>
Smart auto-reply for GitHub Issues with professional customer service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sendwealth](https://clawhub.ai/user/sendwealth) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Repository maintainers and customer-facing teams use this skill to configure automatic GitHub Issue replies for new customer requests, bug reports, and feature requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic replies post public comments on GitHub Issues. <br>
Mitigation: Confirm public auto-comments are appropriate for the repository and review every reply template before enabling the workflow. <br>
Risk: Broad GitHub Actions permissions can allow more repository access than the reply workflow needs. <br>
Mitigation: Use least-privilege workflow permissions for issue comments and pin or allowlist the GitHub Action. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/sendwealth/github-auto-reply) <br>
- [Publisher profile](https://clawhub.ai/user/sendwealth) <br>
- [Publisher website](https://sendwealth.github.io/claw-intelligence/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML and JavaScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces GitHub Actions workflow snippets and issue comment templates; no runtime service is bundled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
