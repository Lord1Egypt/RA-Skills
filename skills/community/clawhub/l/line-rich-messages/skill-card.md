## Description: <br>
A comprehensive guide for LINE Rich UI features that helps agents provide professional, low-friction LINE experiences with Flex Messages, buttons, quick replies, and markdown auto-conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shingo0620](https://clawhub.ai/user/shingo0620) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to shape LINE agent responses into rich, low-friction UI messages with Flex cards, buttons, quick replies, and markdown-to-Flex conversion guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: README text still contains obsolete file-delivery references even though the file-delivery workflow was removed. <br>
Mitigation: Treat file upload or sharing as out of scope for this skill; use a separate tightly scoped workflow with explicit allowlists and safeguards if file delivery is required. <br>
Risk: Generated button labels, actions, and URLs can cause users to open unintended links or send unintended commands. <br>
Mitigation: Review labels, URLs, and message actions before sending rich LINE messages. <br>
Risk: LINE Flex Message text cannot be selected or copied by users. <br>
Mitigation: Send copy-sensitive values such as IDs, keys, tokens, and long URLs as plain text rather than Flex cards or auto-converted markdown. <br>
Risk: Broad inline-button capability can expose rich-message interactions outside the intended LINE context. <br>
Mitigation: Scope LINE inline-button capability to DMs or the intended contexts when possible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shingo0620/line-rich-messages) <br>
- [LINE UI Decision Matrix](references/decision-matrix.md) <br>
- [LINE Directives Guide](references/directives.md) <br>
- [LINE Flex Message Templates](references/flex-templates.md) <br>
- [LINE Markdown Auto-Conversion](references/markdown-to-flex.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with LINE directive examples and JSON Flex Message templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenClaw LINE plugin setup for LINE-specific directives to render.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
