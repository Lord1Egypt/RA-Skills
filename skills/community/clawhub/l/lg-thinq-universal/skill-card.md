## Description:

Universal LG ThinQ device setup and control that discovers appliances and generates device-specific OpenClaw skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utkarshthedev](https://clawhub.ai/user/utkarshthedev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and home automation developers use this skill to connect LG ThinQ accounts, discover linked appliances, and generate isolated device-specific skills for appliance setup and control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an LG account personal access token.

Mitigation: Keep LG_PAT in a protected shell environment or secret manager and do not paste it into chat or copy it into generated device skill directories.

Risk: API server routing can be overridden or cached.

Mitigation: Do not set LG_API_SERVER unless the destination is trusted, and inspect .api_server_cache before use.

Risk: Generated device skills and shell commands can control real appliances.

Mitigation: Review generated files and command manifests before approving execution.

Risk: The workflow may persist setup details to memory.

Mitigation: Approve memory persistence only when the exact entry is shown and limited to the minimum useful device-skill details.

## Reference(s):

- [LG ThinQ Universal Skill README](artifact/README.md)
- [LG ThinQ API: Technical Reference](artifact/references/api-reference.md)
- [Manual Setup Guide](artifact/references/manual-setup.md)
- [LG Device Skill: Complete Example](artifact/references/device-example.md)
- [LG Device Skill Template](artifact/references/device-skill-template.md)
- [LG Device Skill Generation Guide](artifact/references/skill-generation-guide.md)
- [LG ThinQ PAT Portal](https://connect-pat.lgthinq.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, generated files, and JSON device data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate device-specific skill files and command scripts after user approval.]

## Skill Version(s):

1.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
