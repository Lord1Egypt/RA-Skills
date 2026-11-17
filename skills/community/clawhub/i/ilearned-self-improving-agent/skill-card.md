## Description:

Use ilearned as persistent rule-book memory to find, apply, verify, and refine reusable lessons for future tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerrywang121](https://clawhub.ai/user/jerrywang121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to search for relevant past lessons before work and capture verified, reusable rules after corrections, failures, or better approaches. It helps keep durable memory scoped, checkable, and subordinate to current instructions and verified sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can retain sensitive or incorrect lessons, and the setup guide says the database is plaintext by default.

Mitigation: Keep secrets and raw private transcripts out of memory, and choose the storage location with the intended privacy and sharing boundaries in mind.

Risk: Setup may change client configuration or restart the gateway, and scanner coverage is partial because two local path-like references were unresolved.

Mitigation: Review the target configuration and restart impact before setup, and resolve the two references and inspect the full package before deployment.

## Reference(s):

- [ilearned project homepage](https://github.com/jerrywang121/ilearned)
- [ClawHub skill listing](https://clawhub.ai/jerrywang121/skills/ilearned-self-improving-agent)
- [Setup guide](references/setup.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands]

**Output Format:** [Markdown guidance with structured JSON rule examples, shell commands, and MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rules are scoped and checkable; setup, storage, and shared-memory changes require explicit user permission.]

## Skill Version(s):

0.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
