## Description:

Collects direct-message ideas that start with idea prefixes into Feishu/Lark Bitable, uses a model to summarize, categorize, and tag them, and sends a daily digest when new items exist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanxiaolin](https://clawhub.ai/user/hanxiaolin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to capture personal ideas from Feishu/Lark direct messages, structure them in Bitable, and receive daily summaries for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send private idea text to Feishu/Lark and a configured model provider.

Mitigation: Avoid highly sensitive ideas unless the Feishu/Lark workspace and model provider retention policies are acceptable.

Risk: The skill reads Codex/OpenClaw model configuration and credentials for model calls.

Mitigation: Use dedicated low-privilege model credentials and review the configured provider before installation.

Risk: The skill creates a Bitable app and saves local configuration.

Mitigation: Review Feishu/Lark permissions and local config file permissions after setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hanxiaolin/skills/idea-inbox)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Configuration]

**Output Format:** [JSON classification output, Feishu/Lark Bitable records, local configuration, and daily digest messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs only for configured direct-message prefixes, writes Bitable records, and returns either a record_id or an error reason.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
