## Description:

Turns a supplied still image into a short, directed image-to-video clip and guides review of the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use the skill to animate a supplied photo, product image, portrait, illustration, or artwork into a short video clip, then review the result for visual drift and motion quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connection requests unrelated music, speech, voice-management, and spending permissions.

Mitigation: Review the requested permissions before approval and ask the publisher to narrow the authorization.

Risk: Selected images are uploaded externally, and installation/device details are reported automatically.

Mitigation: Avoid uploading sensitive images and review the data-sharing behavior before installing or using the skill.

Risk: Removing the skill can mistakenly disconnect other Beatra skills if installation inventory is inaccurate.

Mitigation: Check other Beatra installations before removal and use the Beatra Console when confirmed revocation is needed.

## Reference(s):

- [Image to Motion on ClawHub](https://clawhub.ai/beatra-ai/skills/image-to-motion)
- [Beatra MCP service](https://mcp.beatra.ai/mcp)
- [Workflow](references/workflow.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Updates and security](references/updates-and-security.md)
- [MCP connection](references/mcp-connection.md)
- [Tasks and results](references/tasks-and-results.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Video, Guidance]

**Output Format:** [Short image-to-video clip with concise text task status and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One supplied still image per clip; review the generated video for visual drift and motion quality.]

## Skill Version(s):

0.2.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
