## Description: <br>
Send WhatsApp messages to other people or search/sync WhatsApp history via the wacli CLI (not for normal user chats). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gabrielsayumi](https://clawhub.ai/user/gabrielsayumi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to operate the wacli CLI for explicit WhatsApp messaging requests and for searching, syncing, or backfilling WhatsApp history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The external wacli CLI can access a user's WhatsApp account and locally synced message history. <br>
Mitigation: Install only from trusted sources, complete QR login intentionally, and treat the local wacli store as sensitive account data. <br>
Risk: The agent can send WhatsApp messages or attachments to other people when directed. <br>
Mitigation: Require an explicit recipient and message or file, clarify ambiguity, and confirm the recipient, content, and attachment before sending. <br>


## Reference(s): <br>
- [PROBAR on ClawHub](https://clawhub.ai/gabrielsayumi/probar) <br>
- [wacli homepage](https://wacli.sh) <br>
- [wacli Go module install target](https://github.com/steipete/wacli/cmd/wacli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external wacli binary and explicit user confirmation before sending WhatsApp messages or attachments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
