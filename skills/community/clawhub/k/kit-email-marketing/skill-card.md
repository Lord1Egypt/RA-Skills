## Description: <br>
Run email marketing campaigns via Kit (formerly ConvertKit). Manage subscribers, create broadcasts and sequences, handle tags and segments, track email stats, and automate workflows with webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and email marketing operators use this skill to manage Kit subscribers, tags, broadcasts, sequences, segments, forms, analytics, and webhooks through a connected Kit account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage real Kit email-marketing data through a connected account. <br>
Mitigation: Install only when comfortable connecting Kit through ClawLink, and review write previews before allowing changes. <br>
Risk: Broadcast creation can send, schedule, or publish email content. <br>
Mitigation: Confirm the broadcast content, audience, timing, and public setting before execution. <br>
Risk: Subscriber, tag, broadcast, custom-field, and webhook deletion can affect production marketing workflows. <br>
Mitigation: Verify the target resource with read/list operations first and require explicit confirmation for destructive actions. <br>


## Reference(s): <br>
- [Kit API Documentation](https://api.kit.com/) <br>
- [Kit Broadcasts Guide](https://kit.com/creators/broadcasts) <br>
- [Kit Sequences Guide](https://kit.com/creators/sequences) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [Kit skill page](https://clawhub.ai/hith3sh/kit-email-marketing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API Calls] <br>
**Output Format:** [Markdown with inline shell commands and tool-call parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected Kit account through ClawLink before authenticated Kit tool calls can run.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
