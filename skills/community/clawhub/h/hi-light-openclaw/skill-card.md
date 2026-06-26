## Description: <br>
Install, configure, and troubleshoot the HiLight OpenClaw plugin as a user-facing setup workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gongcong](https://clawhub.ai/user/Gongcong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect OpenClaw to HiLight by installing the HiLight plugin, writing the hi-light channel configuration, updating credentials or websocket settings, and checking gateway restart results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow requires a HiLight API key and writes it into OpenClaw channel configuration. <br>
Mitigation: Treat the API key as sensitive input, avoid echoing it in assistant responses or shared logs, and use credential rotation if exposure is suspected. <br>
Risk: The default channel configuration uses an open direct-message policy and allows messages from any source. <br>
Mitigation: Review the channel policy before deployment and restrict --dm-policy and --allow-from when a narrower access pattern is appropriate. <br>
Risk: The skill installs an external HiLight plugin package. <br>
Mitigation: Install only when the publisher and package are trusted, and review the plugin behavior before use in sensitive environments. <br>


## Reference(s): <br>
- [User Flow](references/user-flow.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Gongcong/hi-light-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request a HiLight API key as sensitive input and should avoid echoing the token in responses.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
