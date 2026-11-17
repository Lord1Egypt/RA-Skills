## Description:

Lingxi is an AI orchestration skill that interprets user intent, routes work across models, skills, and tools, coordinates multi-step tasks, and summarizes results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-scarlett](https://clawhub.ai/user/ai-scarlett)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Lingxi to route multi-step user requests across specialized agents for content creation, image generation, code, data analysis, search, translation, task tracking, and dashboard-backed operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes broad orchestration with auto-execution, publishing, remote dashboard access, and persistent task or memory storage.

Mitigation: Review before installation, keep dashboard access local or behind trusted TLS, VPN, or SSH controls, and disable publishing or remote channels until authentication, confirmation, deletion, and audit controls are defined.

Risk: Optional integrations require dashboard, GitHub, bot, and model provider credentials.

Mitigation: Avoid tokens in URLs or source files, store credentials with restricted permissions, pin and inspect dependencies, and grant only the minimum permissions needed for each integration.

Risk: Memory and task retention may store user inputs or operational records.

Mitigation: Constrain or disable retention unless users explicitly agree to storage, and provide review and deletion procedures for retained records.

## Reference(s):

- [Lingxi ClawHub skill page](https://clawhub.ai/ai-scarlett/skills/lingxi-ai)
- [Complex Task Three-Step Methodology](https://mp.weixin.qq.com/s/jnipYTffY_KSfWjqXbyqPQ)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task plans, routed agent outputs, dashboard operation guidance, troubleshooting steps, and implementation snippets.]

## Skill Version(s):

0.1.5 (source: server release metadata; artifact documents Lingxi v3.3.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
