## Description:

WhatsApp表情搜索 helps agents search Tenor and Giphy for GIF reactions, convert selected GIFs to WhatsApp-compatible MP4 files, and send them to a specified WhatsApp contact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External personal WhatsApp users use this skill to find a GIF reaction, convert it into a playable MP4, and send it to one selected WhatsApp recipient from an agent environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mismatched routing text could cause the skill to be invoked for SEO or generic automation tasks outside its WhatsApp GIF purpose.

Mitigation: Use the skill only for explicit WhatsApp GIF search, conversion, and sending requests; route SEO or search-traffic work to a different skill.

Risk: The skill can guide an agent to send media to an external WhatsApp recipient.

Mitigation: Confirm the recipient and selected media file before any send action.

Risk: The workflow downloads remote GIF media and converts it with command-line tools.

Mitigation: Review commands before execution, keep tool inputs scoped to the selected GIF URL, and use the platform workspace path required for message sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/gif-whatsapp-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent through GIF search, download, MP4 conversion, workspace file placement, and WhatsApp message sending.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
