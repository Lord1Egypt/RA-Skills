## Description:

NanoClaw runtime traffic monitoring baseline for host-side proxy inspection with container-safe MCP and IPC status surfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this scaffold to implement opt-in NanoClaw runtime traffic monitoring for host-managed proxy inspection, redacted findings, and container-safe MCP status surfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Readers may mistake this scaffold for a finished runtime monitor.

Mitigation: Treat it as a specification baseline until proxy, MCP, IPC, tests, and release controls are implemented and reviewed.

Risk: Future HTTPS inspection could expose CA private key material or raw traffic to containers.

Mitigation: Keep CA keys host-side, require explicit per-runtime trust configuration, and expose only redacted status and findings through container-facing surfaces.

Risk: Future monitoring could persist sensitive request or response snippets.

Mitigation: Redact secrets before writing JSONL findings or returning MCP responses, and keep scan byte limits bounded and configurable.

Risk: Automatic trust-store changes or blocking behavior could disrupt operator environments.

Mitigation: Keep monitoring opt-in, detect-and-log by default, avoid automatic system CA installation, and leave blocking out of the first implementation.

## Reference(s):

- [ClawSec homepage](https://clawsec.prompt.security)
- [NanoClaw Traffic Guardian page](https://clawhub.ai/davida-ps/skills/nanoclaw-traffic-guardian)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON examples and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spec scaffold only; this release does not include active proxy, persistence, or runtime enforcement code.]

## Skill Version(s):

0.0.1-beta2 (source: frontmatter, skill.json, changelog, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
