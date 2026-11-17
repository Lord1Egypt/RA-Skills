## Description:

Automated monthly photo-to-Mixtiles pipeline. Collects photos from a WhatsApp group, curates the best ones using vision, builds a multi-photo Mixtiles cart link, and sends it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saharcarmel](https://clawhub.ai/user/saharcarmel)

### License/Terms of Use:


## Use Case:

External users use this skill to collect recent family photos from a WhatsApp group, choose suitable images for a monthly Mixtiles order, generate a cart link, and send that link to a configured recipient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private WhatsApp photos and message metadata.

Mitigation: Run it only for groups the user is authorized to process, keep downloaded files in a controlled location, and delete local queues after the order workflow is complete.

Risk: The collection step can gather photos outside the intended monthly window because the script filters only by a lower date bound.

Mitigation: Review the downloaded manifest and selected files before upload or sending, and add an explicit upper date bound before relying on unattended monthly execution.

Risk: Selected photos may be uploaded to Cloudinary and shared through a Mixtiles cart link with limited user control.

Mitigation: Confirm selected images, upload destination, cart contents, and recipient before sending the link.

Risk: The newest-file fallback can associate a downloaded file with the wrong message if structured download output is missing.

Mitigation: Prefer verified media download paths from wacli output and inspect the manifest when fallback path detection is used.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/saharcarmel/skills/i-love-you-mom)
- [Publisher profile](https://clawhub.ai/user/saharcarmel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command blocks and a JSON manifest from the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires wacli, jq, python3, WhatsApp group configuration, and a compatible Mixtiles cart script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
