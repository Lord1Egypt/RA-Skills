## Description:

Oktk compresses CLI outputs for git, Docker, Kubernetes, tests, file listings, network calls, and searches before they are sent to an LLM to reduce token usage and API cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satnamra](https://clawhub.ai/user/satnamra)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Oktk to summarize verbose terminal output before passing it to an LLM, preserving command status and key details while reducing context and cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper can execute or re-run shell commands, including commands that modify files, install packages, deploy services, or touch Docker and Kubernetes state.

Mitigation: Review commands before using Oktk, and avoid sourcing aliases or using the universal wrapper for state-changing commands.

Risk: Filtered output can still contain sensitive information or omit details needed for exact diagnosis.

Mitigation: Treat filtered summaries as potentially sensitive, review them before sharing with an LLM, and use raw output when full fidelity is required.

Risk: Cache and analytics can retain command metadata or output locally under the user's Oktk directory.

Mitigation: Disable local retention when it is not acceptable, and clear the cache and analytics files when command history or output should not persist.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/satnamra/skills/oktk)
- [Project Homepage](https://github.com/satnamra/openclaw-workspace/tree/main/skills/oktk)
- [Node.js Runtime](https://nodejs.org)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text command-output summaries with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include filtered summaries, cache/statistics reports, and raw output when bypassed.]

## Skill Version(s):

2.4.0 (source: server release metadata, skill frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
