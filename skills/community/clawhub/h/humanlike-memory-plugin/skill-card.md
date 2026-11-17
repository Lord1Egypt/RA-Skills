## Description:

Long-term memory plugin for OpenClaw: automatic recall, storage, and agent tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[humanlike2026](https://clawhub.ai/user/humanlike2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this plugin to give agents long-term memory across sessions, including automatic recall, automatic conversation storage, and agent-callable memory search and storage tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation data is stored and recalled by a remote service by default.

Mitigation: Review before installing in sensitive workspaces, use a test API key first, avoid secrets or regulated data, and set addEnabled=false and recallEnabled=false until the behavior is validated.

Risk: Recalled memories can affect future agent prompts and responses.

Mitigation: Limit use to trusted memory stores, review retrieved context during sensitive tasks, and disable recall when memory injection is not appropriate.

Risk: <private> tags should not be treated as a transmission control.

Mitigation: Do not place sensitive content in conversations sent to the plugin; use configuration controls such as addEnabled=false instead of relying on tags.

Risk: Using an untrusted API endpoint could expose conversation content.

Mitigation: Use only the official HTTPS endpoint unless operating a controlled service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/humanlike2026/skills/humanlike-memory-plugin)
- [Human-Like Memory service](https://plugin.human-like.me)
- [npm package](https://www.npmjs.com/package/@humanlikememory/human-like-mem)
- [Source repository](https://gitlab.ttyuyin.com/personalization_group/human-like-mem-openclaw-plugin)
- [README](artifact/README.md)
- [Security and Data Transparency](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [text, configuration, API calls, guidance]

**Output Format:** [Agent-readable memory search results, OpenClaw configuration values, and remote memory store or recall operations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an API key and OpenClaw >=2026.2.0. Recall and storage are enabled by default unless configured otherwise.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
