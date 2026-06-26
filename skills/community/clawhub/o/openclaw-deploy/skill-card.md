## Description: <br>
Builds and packages OpenClaw deployments as Docker images or portable clean and full release bundles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zfanmy](https://clawhub.ai/user/zfanmy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to build OpenClaw Docker images or portable packages, deploy clean or full variants to servers, and support backup or migration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The full-package workflow can bundle local OpenClaw tokens, configuration, conversation history, workspace data, and other secrets for transfer. <br>
Mitigation: Use the clean package unless a full migration is intentional; inspect and redact ~/.openclaw before building or transferring full packages, protect archives in transit, and rotate copied credentials as needed. <br>
Risk: The builder writes to and removes the configured output directory. <br>
Mitigation: Verify OUTPUT_DIR points to a safe disposable location before running the builder. <br>
Risk: The Node/NVM installer fetches and executes an external installation script. <br>
Mitigation: Review the installer before executing it in the target environment. <br>


## Reference(s): <br>
- [Openclaw Deploy ClawHub Page](https://clawhub.ai/zfanmy/openclaw-deploy) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [Artifact README.md](artifact/README.md) <br>
- [Artifact Templates README.md](artifact/templates/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, configuration examples, and deployment guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent guidance for building, exporting, importing, and starting OpenClaw deployment packages.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
