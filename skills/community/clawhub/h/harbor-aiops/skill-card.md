## Description:

Use this skill when a user asks to inspect Harbor projects, repositories, artifacts, scans, vulnerabilities, quotas, GC, replication or retention, or to start an artifact scan, create a tag or delete one mutable tag.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and registry operators use Harbor AIops to diagnose Harbor health and inspect projects, artifacts, vulnerabilities, storage, garbage collection, replication, and retention. It can also start artifact scans, create tags, or delete a specific mutable tag with guarded checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tag deletion is high risk and has no safe general undo.

Mitigation: Use a dry run, verify the exact tag, digest, and mutable state, and confirm absence afterward; if the result is unknown, read current state before retrying.

Risk: Scan and tag writes can have unknown outcomes when acceptance or post-write verification is incomplete.

Mitigation: Check the Harbor job and current state before retrying, and do not treat an execution ID alone as proof of success.

Risk: Harbor credentials could be exposed if Basic authentication is sent over plaintext HTTP.

Mitigation: Use HTTPS with certificate validation and a narrowly scoped robot account; do not send Basic credentials over plaintext networks.

Risk: Failed, unauthorized, or truncated probes can be mistaken for empty or complete results.

Mitigation: Inspect error, complete, and truncated indicators before drawing conclusions from a probe or list.

## Reference(s):

- [Harbor AIops project homepage](https://github.com/AIops-tools/Harbor-AIops)
- [Harbor AIops ClawHub release](https://clawhub.ai/zw008/skills/harbor-aiops)
- [Agent guardrails](artifact/references/agent-guardrails.md)
- [Capabilities](artifact/references/capabilities.md)
- [CLI reference](artifact/references/cli-reference.md)
- [Setup guide](artifact/references/setup-guide.md)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown diagnostic summaries, guidance, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Harbor inventory and operation status; write outcomes may be reported as unknown when verification is incomplete.]

## Skill Version(s):

0.2.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
