## Description:

Extract readable content from webpages with a stable, low-dependency workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ylkangpeter](https://clawhub.ai/user/ylkangpeter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to open, inspect, summarize, translate, verify, or quote public web pages while reporting the extraction method and any access limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs from the agent runtime, which may expose private services, localhost tools, or cloud metadata endpoints if used in a privileged network.

Mitigation: Use it only for trusted public URLs or run it in a network-restricted environment that cannot reach private infrastructure.

Risk: The skill can accept raw session cookies for some fetch paths, and command-line secrets may leak through process or tool logs.

Mitigation: Avoid passing real account cookies unless the target is trusted and the runtime protects command arguments and logs.

Risk: Some pages may return only metadata, fragments, login walls, CAPTCHA, regional blocks, or anti-bot responses.

Mitigation: Report the extraction method and limitations clearly, and do not imply full page access when only partial content was recovered.

## Reference(s):

- [Page Fetch Skill Page](https://clawhub.ai/ylkangpeter/skills/page-fetch)
- [Page Fetch Strategy](artifact/references/strategy.md)
- [Browser Runtime Notes](artifact/references/browser-runtime.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON extraction output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports extraction method, recovered page metadata, body text or summary, and known access limitations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
