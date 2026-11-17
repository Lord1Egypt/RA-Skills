## Description:

Persistent memory system for AI agents with automatic encoding, decay, and semantic reinforcement based on Stanford Generative Agents (Park et al., 2023).

This skill is ready for commercial/non-commercial use.

## Publisher:

[impkind](https://clawhub.ai/user/impkind)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Hippocampus to give OpenClaw agents persistent, searchable memory with importance scoring, scheduled encoding, decay, and semantic reinforcement. It supports session-start memory loading, recall queries, memory consolidation, and dashboard generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent conversation scanning and plaintext memory storage can retain sensitive personal data or secrets.

Mitigation: Review privacy fit before installation, avoid use around secrets or sensitive personal data, and avoid whole-history processing unless explicitly intended.

Risk: Optional cron processing can repeatedly summarize conversations into persistent memory without active review.

Mitigation: Enable scheduled encoding or decay only when background memory processing is intended and reviewed.

Risk: The security evidence reports exploitable local scripting and dashboard-rendering issues.

Mitigation: Fix code-injection, prompt-injection, dashboard escaping, retention, permissions, approval, and deletion controls before sensitive or trusted deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/impkind/skills/hippocampus-memory)
- [Publisher Profile](https://clawhub.ai/user/impkind)
- [GitHub Repository](https://github.com/ImpKind/hippocampus-skill)
- [Stanford Generative Agents Paper](https://arxiv.org/abs/2304.03442)
- [Generative Agents Reference Implementation](https://github.com/joonspk-research/generative_agents)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown and shell command output, plus generated JSON, Markdown, and HTML files in the configured workspace.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent plaintext memory files under WORKSPACE and can optionally schedule recurring encoding and decay jobs.]

## Skill Version(s):

3.8.6 (source: server release, openclaw metadata, and changelog released 2026-02-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
