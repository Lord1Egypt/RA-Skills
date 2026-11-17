## Description:

Model-agnostic WhatsApp @mention skill for OpenClaw that converts @Name, @Phone, and @LID to blue clickable WhatsApp mentions with any AI model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junwei1213](https://clawhub.ai/user/junwei1213)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw bot operators and developers use this skill to make WhatsApp group @mentions reliable across AI models by converting names, phone numbers, and LIDs into WhatsApp-compatible mention text and metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer patches OpenClaw's installed JavaScript messaging files.

Mitigation: Review install.sh before installation, keep the generated backups, and use uninstall.sh to restore the patched files if behavior is unexpected.

Risk: Installation can restart the OpenClaw service and interrupt active bot operation.

Mitigation: Install during a maintenance window and verify the service status after installation.

Risk: The skill stores WhatsApp contact and group identity mappings in LID_CACHE.json.

Mitigation: Restrict file permissions on LID_CACHE.json and avoid adding unnecessary contact or group data.

Risk: Running add-member.js with a phone number and no --group can update every cached group.

Mitigation: Use --group for targeted updates unless updating all cached groups is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/junwei1213/skills/openclaw-mention-skill)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [WhatsApp message text with mention metadata, plus Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mention conversion depends on the local LID cache and the current WhatsApp group context.]

## Skill Version(s):

1.0.1 (source: release evidence; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
