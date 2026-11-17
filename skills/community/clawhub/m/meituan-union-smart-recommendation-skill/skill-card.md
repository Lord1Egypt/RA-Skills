## Description:

A Meituan lifestyle-service shopping guide that identifies user needs and returns venue links for food delivery, flash shopping, restaurant group-buying, leisure services, and medicine delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meituan-union](https://clawhub.ai/user/meituan-union)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill inside an AI agent to get Meituan service recommendations and venue links after account authorization and media-code binding.

### Deployment Geography for Use:

Chinese mainland

## Known Risks and Mitigations:

Risk: The skill authenticates to Meituan and stores account-linked local authorization and binding data.

Mitigation: Install only from a trusted publisher, use it in a trusted agent environment, review the service rules before authorizing, and clear local token or binding data when access is no longer needed.

Risk: The skill can make persistent local or global changes, including local state files and global npm environment changes.

Mitigation: Review the setup scripts before use, run the skill in an isolated user profile when possible, and remove installed dependencies and local state during decommissioning.

Risk: The skill can show promotional venue links and perform background update checks.

Mitigation: Verify link destinations and publisher trust before following recommendations, and apply network controls if background checks are not acceptable for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meituan-union/skills/meituan-union-smart-recommendation-skill)
- [Skill service rules](references/terms-of-service.md)
- [Self-diagnosis guide](references/DOCTOR.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with venue links and local command workflows for authorization, binding, diagnostics, and setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include user-facing recommendation text, authorization prompts, QR-code or link display, and diagnostic guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
